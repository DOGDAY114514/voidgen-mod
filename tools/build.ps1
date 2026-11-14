$ErrorActionPreference = "Stop"

$Root = "D:\AI\voidgen-mod"
$Jdk = "D:\jdk-21"
$PatchedJar = "C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_719987e3c5f5d9e2c827822e1813d4a73b19efd6_output.jar"
# AE2 19.2.18 reference jar (compile-only; not bundled into the mod).
$Ae2Jar = Join-Path $Root "libs\compile-only\appliedenergistics2-19.2.18.jar"
$Build = Join-Path $Root "build"

Write-Host "[1/4] clean"
Remove-Item -Recurse -Force $Build -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force (Join-Path $Build "stubs"), (Join-Path $Build "classes"), (Join-Path $Build "jar") | Out-Null

Write-Host "[2/4] compile stubs"
$StubSources = Get-ChildItem -Path (Join-Path $Root "stubs") -Recurse -Filter *.java | ForEach-Object FullName
& (Join-Path $Jdk "bin\javac.exe") -encoding UTF-8 -source 21 -target 21 -d (Join-Path $Build "stubs") $StubSources
if ($LASTEXITCODE -ne 0) { throw "stub compile failed" }

Write-Host "[3/4] compile mod"
$Sources = Get-ChildItem -Path (Join-Path $Root "src\main\java") -Recurse -Filter *.java | ForEach-Object FullName

# Minecraft runtime libraries (Gradle distribution ships all of these; the
# NeoForge jar itself assumes them on the classpath).
$GradleLib = "C:\Users\Administrator\.gradle\wrapper\dists\gradle-9.2.1-bin\2t0n5ozlw9xmuyvbp7dnzaxug\gradle-9.2.1\lib"
$LibJars = @(
    "slf4j-api-2.0.17.jar",
    "guava-33.4.6-jre.jar",
    "failureaccess-1.0.3.jar",
    "gson-2.13.1.jar",
    "fastutil-8.5.2-min.jar",
    "commons-io-2.15.1.jar",
    "commons-lang3-3.17.0.jar",
    "commons-codec-1.18.0.jar",
    "httpclient-4.5.14.jar",
    "httpcore-4.4.14.jar",
    "javax.inject-1.jar",
    "jsr305-3.0.2.jar",
    "annotations-24.0.1.jar"
) | ForEach-Object { Join-Path $GradleLib $_ }

$Classpath = "$PatchedJar;$(Join-Path $Build "stubs")" + ";" + ($LibJars -join ";") + ";" + $Ae2Jar
& (Join-Path $Jdk "bin\javac.exe") -encoding UTF-8 -source 21 -target 21 -cp $Classpath -d (Join-Path $Build "classes") $Sources
if ($LASTEXITCODE -ne 0) { throw "mod compile failed" }

Write-Host "[4/4] package"
Copy-Item -Recurse -Force (Join-Path $Build "classes\*") (Join-Path $Build "jar")
Copy-Item -Recurse -Force (Join-Path $Root "src\main\resources\*") (Join-Path $Build "jar")
New-Item -ItemType Directory -Force (Join-Path $Root "dist") | Out-Null
$OutJar = Join-Path $Root "dist\voidgen-2.3.7.jar"
& (Join-Path $Jdk "bin\jar.exe") --create --file $OutJar -C (Join-Path $Build "jar") .
if ($LASTEXITCODE -ne 0) { throw "jar failed" }
Write-Host "OK: $OutJar"

