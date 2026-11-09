# Hitung nomor halaman DAFTAR ISI / TABEL / GAMBAR untuk PROPOSAL_SEMPRO_BAB_I_III.docx
# Memakai Word COM (tanpa dependensi Python tambahan).
# Alur: generate_sempro_study2.py -> skrip ini -> generate_sempro_study2.py (ulang).

$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..\..")
$docx = Join-Path $root "03_Naskah_Skripsi\study2\PROPOSAL_SEMPRO_BAB_I_III.docx"
$keysPath = Join-Path $here "toc_keys_sempro.json"
$outPath = Join-Path $here "toc_pages_sempro.json"

if (-not (Test-Path $docx)) { throw "DOCX belum ada: $docx" }
if (-not (Test-Path $keysPath)) { throw "Daftar kunci belum ada: $keysPath" }

$keys = Get-Content $keysPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Salin ke temp agar tidak bentrok bila file sedang dibuka Word
$tmp = Join-Path $env:TEMP "sempro_toc_pages.docx"
Copy-Item $docx $tmp -Force

function ConvertTo-Roman([int]$n) {
    $pairs = @(
        @(10, "x"), @(9, "ix"), @(5, "v"), @(4, "iv"), @(1, "i")
    )
    $s = ""
    foreach ($p in $pairs) {
        while ($n -ge $p[0]) { $s += $p[1]; $n -= $p[0] }
    }
    return $s
}

function Find-Page($doc, [int]$startPos, [int]$endPos, [string]$needle, [bool]$last, [bool]$caption = $false) {
    $searchStart = $startPos
    $found = $null
    while ($true) {
        $rng = $doc.Range($searchStart, $endPos)
        $find = $rng.Find
        $find.ClearFormatting()
        $find.Text = $needle
        $find.Forward = $true
        $find.Wrap = 0            # wdFindStop
        $find.MatchCase = $true
        $find.MatchWildcards = $false
        if (-not $find.Execute()) { break }
        $paraText = $rng.Paragraphs.Item(1).Range.Text.Trim()
        $isMatch = if ($caption) { $paraText.Contains($needle) } else { $paraText -eq $needle }
        if ($isMatch) {
            $found = $rng.Information(3)   # wdActiveEndPageNumber
            if (-not $last) { break }
        }
        $searchStart = $rng.End
        if ($searchStart -ge $endPos) { break }
    }
    return $found
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($tmp, $false, $true)
    $doc.Repaginate()

    $sec1 = $doc.Sections.Item(1).Range
    $sec2 = $doc.Sections.Item(2).Range
    $s1Start = $sec1.Start
    $s1End = $sec1.End
    $s2Start = $sec2.Start
    $s2End = $sec2.End

    $raw = @{}
    foreach ($k in $keys) {
        $needle = [string]$k.key
        if ($needle.Length -eq 0) { continue }
        if ($k.scope -eq "front") {
            $p = Find-Page $doc $s1Start $s1End $needle $true $false
        } else {
            $isCaption = $needle.StartsWith("Tabel ") -or $needle.StartsWith("Gambar ") -or $needle.StartsWith("Lampiran ")
            $p = Find-Page $doc $s2Start $s2End $needle $false $isCaption
        }
        if ($null -eq $p) {
            Write-Warning "Tidak ditemukan: $needle"
        } else {
            $raw[$needle] = [int]$p
        }
    }

    $firstBody = $raw["PENDAHULUAN"]
    if ($null -eq $firstBody) { throw "Halaman BAB I tidak terdeteksi" }
    $offset = $firstBody - 1

    $map = [ordered]@{}
    foreach ($k in $keys) {
        $needle = [string]$k.key
        if (-not $raw.ContainsKey($needle)) { continue }
        $p = $raw[$needle]
        if ($k.scope -eq "front") {
            $map[$needle] = ConvertTo-Roman $p
        } else {
            $map[$needle] = [string]($p - $offset)
        }
    }

    $json = $map | ConvertTo-Json -Depth 3
    [System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "TOC pages -> $outPath (offset=$offset)"
}
finally {
    if ($doc) { $doc.Close($false) }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
