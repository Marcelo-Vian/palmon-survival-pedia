param(
    [switch]$SkipPush,
    [string]$ZipPath
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$LogDir = Join-Path $Root "logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$LogFile = Join-Path $LogDir ("update-shop-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".log")

function Write-Step([string]$Text) {
    Write-Host ""
    Write-Host "== $Text ==" -ForegroundColor Cyan
}

function Fail([string]$Text) {
    throw $Text
}

function Resolve-Python {
    $bundled = "C:\Users\marce\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $bundled) { return $bundled }
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $cmd) { return $cmd.Source }
    Fail "Python nao encontrado. Abra no Codex para eu corrigir o caminho."
}

function Run-Checked([string]$Exe, [string[]]$ArgsList) {
    Write-Host ("> " + $Exe + " " + ($ArgsList -join " ")) -ForegroundColor DarkGray
    & $Exe @ArgsList
    if ($LASTEXITCODE -ne 0) {
        Fail "Comando falhou com codigo ${LASTEXITCODE}: $Exe $($ArgsList -join ' ')"
    }
}

function Get-SafeToken([string]$Text) {
    $safe = [regex]::Replace($Text, "[^A-Za-z0-9._-]", "_")
    if ([string]::IsNullOrWhiteSpace($safe)) { return "arquivo" }
    return $safe
}

function Import-ShopZip([string]$CandidateZip, [string]$ZipDropDir, [string]$PrintsDir) {
    New-Item -ItemType Directory -Path $ZipDropDir -Force | Out-Null
    New-Item -ItemType Directory -Path $PrintsDir -Force | Out-Null

    $SelectedZip = $null
    if (-not [string]::IsNullOrWhiteSpace($CandidateZip)) {
        $ResolvedZip = Resolve-Path -LiteralPath $CandidateZip -ErrorAction SilentlyContinue
        if ($null -eq $ResolvedZip) {
            Fail "ZIP nao encontrado: $CandidateZip"
        }
        $SelectedZip = Get-Item -LiteralPath $ResolvedZip.Path
    }
    else {
        $ZipFiles = @(Get-ChildItem -Path $ZipDropDir -Filter "*.zip" -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending)
        if ($ZipFiles.Count -gt 0) {
            $SelectedZip = $ZipFiles[0]
        }
    }

    if ($null -eq $SelectedZip) {
        Write-Host "Nenhum ZIP encontrado em: $ZipDropDir"
        Write-Host "Vou atualizar o site com a base atual."
        return 0
    }

    if ($SelectedZip.Extension.ToLowerInvariant() -ne ".zip") {
        Fail "Arquivo informado nao e ZIP: $($SelectedZip.FullName)"
    }

    Write-Host "ZIP encontrado: $($SelectedZip.FullName)"
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $ExtractRoot = Join-Path $ZipDropDir "extracted"
    $ExtractDir = Join-Path $ExtractRoot ($Stamp + "-" + (Get-SafeToken $SelectedZip.BaseName))
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null

    Expand-Archive -LiteralPath $SelectedZip.FullName -DestinationPath $ExtractDir -Force

    $AllowedExtensions = @(".png", ".jpg", ".jpeg", ".webp")
    $Images = @(Get-ChildItem -Path $ExtractDir -Recurse -File | Where-Object { $AllowedExtensions -contains $_.Extension.ToLowerInvariant() })
    if ($Images.Count -eq 0) {
        Write-Warning "ZIP extraido, mas nenhuma imagem PNG/JPG/JPEG/WEBP foi encontrada dentro dele."
        return 0
    }

    $Index = 0
    foreach ($Image in $Images) {
        $Index += 1
        $TargetName = "{0}_{1}_{2}" -f $Stamp, $Index.ToString("000"), (Get-SafeToken $Image.Name)
        Copy-Item -LiteralPath $Image.FullName -Destination (Join-Path $PrintsDir $TargetName) -Force
    }

    Write-Host "Imagens importadas para prints: $($Images.Count)" -ForegroundColor Green
    Write-Warning "Se essas imagens tiverem pacotes novos, ainda preciso transformar os prints em dados no JSON para aparecerem na tabela."
    return $Images.Count
}

Start-Transcript -Path $LogFile -Force | Out-Null

try {
    Write-Host "Palmon Survival - atualizacao 1 clique da loja" -ForegroundColor Green
    Write-Host "Pasta: $Root"
    Write-Host "Log: $LogFile"

    $PrintsDir = "D:\Linkedin\palmon_survival_prints\loja\prints"
    $ZipDropDir = Join-Path $Root "COLOQUE_O_ZIP_AQUI"

    Write-Step "Importar ZIP de prints"
    $ImportedImageCount = Import-ShopZip $ZipPath $ZipDropDir $PrintsDir
    Write-Host "Imagens novas importadas nesta execucao: $ImportedImageCount"

    Write-Step "Selecionar base de dados mais recente"
    $DataFiles = @(Get-ChildItem -Path $Root -Filter "shop_active_offers_*.json" -File | Sort-Object LastWriteTime -Descending)
    if ($DataFiles.Count -eq 0) {
        Fail "Nenhum shop_active_offers_*.json encontrado."
    }
    $DataFile = $DataFiles[0]
    $env:PALMON_SHOP_DATA = $DataFile.Name
    Write-Host "Usando: $($DataFile.Name)"

    if (Test-Path $PrintsDir) {
        $LatestPrint = Get-ChildItem -Path $PrintsDir -File | Where-Object { $_.Extension -match "png|jpg|jpeg|webp" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($null -ne $LatestPrint -and $LatestPrint.LastWriteTime -gt $DataFile.LastWriteTime.AddMinutes(2)) {
            Write-Warning "Existem prints mais novos que o JSON usado. Se forem pacotes novos, eu ainda preciso transformar esses prints em dados antes de publicar."
            Write-Warning "Print mais novo: $($LatestPrint.Name)"
        }
    }

    $Python = Resolve-Python

    Write-Step "Gerar miniaturas dos pacotes"
    Run-Checked $Python @(".\generate_shop_offer_thumbnails.py")

    Write-Step "Reconstruir pagina da loja"
    Run-Checked $Python @(".\build_shop_capture_site.py")

    Write-Step "Atualizar preview da pagina inicial"
    Run-Checked $Python @(".\generate_shop_home_preview.py")

    Write-Step "Validar scripts"
    Run-Checked $Python @("-m", "py_compile", ".\build_shop_capture_site.py", ".\generate_shop_offer_thumbnails.py", ".\generate_shop_home_preview.py")

    Write-Step "Validar HTML gerado"
    $Data = Get-Content -Path $DataFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    $OfferCount = @($Data.offers).Count
    $ThumbCount = @(Get-ChildItem -Path ".\assets\shop_offer_thumbs" -Filter "*.jpg" -File).Count
    $Html = Get-Content -Path ".\palmon_shop_captures.html" -Raw -Encoding UTF8
    $OfferIdsInHtml = [regex]::Matches($Html, '"id"\s*:').Count
    $ThumbRefsInHtml = [regex]::Matches($Html, "assets/shop_offer_thumbs").Count
    $OldPrintRefs = [regex]::Matches($Html, "assets/shop_captures").Count

    if ($OfferCount -le 0) { Fail "JSON sem ofertas." }
    if ($OfferIdsInHtml -ne $OfferCount) { Fail "HTML tem $OfferIdsInHtml ofertas, mas JSON tem $OfferCount." }
    if ($ThumbCount -lt $OfferCount) { Fail "Faltam miniaturas: $ThumbCount JPGs para $OfferCount ofertas." }
    if ($ThumbRefsInHtml -lt $OfferCount) { Fail "HTML tem poucas referencias de miniatura: $ThumbRefsInHtml para $OfferCount ofertas." }
    if ($OldPrintRefs -ne 0) { Fail "HTML voltou a apontar para prints completos antigos." }

    Write-Host "Ofertas: $OfferCount"
    Write-Host "Miniaturas: $ThumbCount"
    Write-Host "Referencias no HTML: $ThumbRefsInHtml"

    Write-Step "Verificar mudancas"
    $Status = git status --short
    if ([string]::IsNullOrWhiteSpace(($Status | Out-String))) {
        Write-Host "Nada mudou. Site ja esta atualizado com a base atual." -ForegroundColor Yellow
        Stop-Transcript | Out-Null
        exit 0
    }
    $Status | ForEach-Object { Write-Host $_ }

    Write-Step "Commitar mudancas"
    git add .gitignore COLOQUE_O_ZIP_AQUI ATUALIZAR_SITE_LOJA_1_CLIQUE.bat COMO_ATUALIZAR_SITE_LOJA.md update_palmon_shop_site.ps1 build_shop_capture_site.py generate_shop_offer_thumbnails.py generate_shop_home_preview.py palmon_shop_captures.html shop_analyzer_screenshot_wide.png shop_active_offers_*.json assets/shop_offer_thumbs
    if ($LASTEXITCODE -ne 0) { Fail "git add falhou." }

    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Nada stageado para commit." -ForegroundColor Yellow
        Stop-Transcript | Out-Null
        exit 0
    }

    $CommitMsg = "Update shop analyzer " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    git commit -m $CommitMsg
    if ($LASTEXITCODE -ne 0) { Fail "git commit falhou." }

    if ($SkipPush) {
        Write-Step "Publicacao ignorada no teste"
        Write-Host "Commit criado localmente. Rode sem -SkipPush para publicar." -ForegroundColor Yellow
    }
    else {
        Write-Step "Publicar no GitHub Pages"
        git push
        if ($LASTEXITCODE -ne 0) { Fail "git push falhou. Verifique login/credenciais do GitHub." }
    }

    Write-Step "Pronto"
    Write-Host "Site publicado:" -ForegroundColor Green
    Write-Host "https://marcelo-vian.github.io/palmon-survival-pedia/palmon_shop_captures.html"
    Write-Host ""
    Write-Host "Se o navegador mostrar cache antigo, use Ctrl+F5 ou acrescente ?v=$(Get-Date -Format yyyyMMddHHmmss)"

    Stop-Transcript | Out-Null
    exit 0
}
catch {
    Write-Host ""
    Write-Host "ERRO: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Log salvo em: $LogFile" -ForegroundColor Yellow
    Stop-Transcript | Out-Null
    exit 1
}
