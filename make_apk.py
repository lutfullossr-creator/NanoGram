#!/usr/bin/env python3
# NanoGram APK loyihasini android/ papkasida yaratadi (GitHub Actions ishlatadi).
import base64, glob, os, shutil, sys

ROOT = 'android'
F = {}

ICON_B64 = """
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
"""

F['settings.gradle.kts'] = r"""pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "NanoGram"
include(":app")
"""

F['build.gradle.kts'] = r"""plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
"""

F['gradle.properties'] = r"""org.gradle.jvmargs=-Xmx2g -Dfile.encoding=UTF-8
android.useAndroidX=false
android.nonTransitiveRClass=true
kotlin.code.style=official
"""

F['app/build.gradle.kts'] = r"""plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

val runNum = (System.getenv("RUN_NUM") ?: "1").toInt()

android {
    namespace = "com.lutfullo.nanogram"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.lutfullo.nanogram"
        minSdk = 26
        targetSdk = 34
        versionCode = runNum
        versionName = "1.0." + runNum
    }

    signingConfigs {
        getByName("debug") {
            val ks = rootProject.file("nanogram.keystore")
            val pw = System.getenv("NG_KS_PASS")
            if (ks.exists() && !pw.isNullOrEmpty()) {
                storeFile = ks
                storePassword = pw
                keyAlias = System.getenv("NG_KS_ALIAS") ?: "edi"
                keyPassword = pw
                storeType = "pkcs12"
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}
"""

F['app/src/main/AndroidManifest.xml'] = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    <uses-permission android:name="android.permission.VIBRATE" />

    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.microphone" android:required="false" />

    <application
        android:label="NanoGram"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher"
        android:allowBackup="false"
        android:usesCleartextTraffic="false"
        android:hardwareAccelerated="true"
        android:theme="@android:style/Theme.DeviceDefault.NoActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTask"
            android:windowSoftInputMode="adjustResize"
            android:configChanges="orientation|screenSize|keyboardHidden|smallestScreenSize|screenLayout|uiMode|density|keyboard|navigation">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

F['app/src/main/java/com/lutfullo/nanogram/MainActivity.kt'] = r"""package com.lutfullo.nanogram

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Color
import android.net.ConnectivityManager
import android.net.Uri
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.JsPromptResult
import android.webkit.JsResult
import android.webkit.PermissionRequest
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText

class MainActivity : Activity() {
    companion object {
        const val URL = "https://nanogrampro.netlify.app/"
        const val HOST = "nanogrampro.netlify.app"
        const val RC_FILE = 9001
        const val RC_WEBPERM = 9003
    }

    private var web: WebView? = null
    private var fileCb: ValueCallback<Array<Uri>>? = null
    private var pendingWeb: PermissionRequest? = null

    private fun online(): Boolean {
        return try {
            val cm = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
            cm.activeNetworkInfo?.isConnected == true
        } catch (e: Exception) { true }
    }

    private fun handleWebPerm(r: PermissionRequest) {
        val need = mutableListOf<String>()
        for (res in r.resources) {
            if (res == PermissionRequest.RESOURCE_VIDEO_CAPTURE) need.add(Manifest.permission.CAMERA)
            if (res == PermissionRequest.RESOURCE_AUDIO_CAPTURE) need.add(Manifest.permission.RECORD_AUDIO)
        }
        val miss = need.filter { checkSelfPermission(it) != PackageManager.PERMISSION_GRANTED }
        if (miss.isEmpty()) { r.grant(r.resources); return }
        pendingWeb?.deny()
        pendingWeb = r
        requestPermissions(miss.toTypedArray(), RC_WEBPERM)
    }

    override fun onRequestPermissionsResult(rc: Int, perms: Array<out String>, res: IntArray) {
        super.onRequestPermissionsResult(rc, perms, res)
        if (rc == RC_WEBPERM) {
            val r = pendingWeb
            pendingWeb = null
            if (r != null) {
                if (res.isNotEmpty() && res.all { it == PackageManager.PERMISSION_GRANTED }) r.grant(r.resources) else r.deny()
            }
        }
    }

    override fun onCreate(b: Bundle?) {
        super.onCreate(b)
        window.statusBarColor = Color.parseColor("#050a14")
        window.navigationBarColor = Color.parseColor("#050a14")
        val w = WebView(this)
        web = w
        setContentView(w)
        w.setBackgroundColor(Color.parseColor("#050a14"))
        val s = w.settings
        s.javaScriptEnabled = true
        s.domStorageEnabled = true
        s.databaseEnabled = true
        s.mediaPlaybackRequiresUserGesture = false
        s.javaScriptCanOpenWindowsAutomatically = true
        s.setSupportMultipleWindows(false)
        s.textZoom = 100
        s.cacheMode = if (online()) WebSettings.LOAD_DEFAULT else WebSettings.LOAD_CACHE_ELSE_NETWORK
        CookieManager.getInstance().setAcceptCookie(true)
        CookieManager.getInstance().setAcceptThirdPartyCookies(w, true)

        w.setDownloadListener { url, _, _, _, _ ->
            try { startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) } catch (e: Exception) {}
        }

        w.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(v: WebView?, r: WebResourceRequest?): Boolean {
                val u = r?.url ?: return true
                val sch = u.scheme ?: ""
                if ((sch == "https" || sch == "http") && u.host == HOST) return false
                if (sch == "file" || sch == "blob" || sch == "data") return false
                if (sch == "http" || sch == "https" || sch == "tel" || sch == "mailto") {
                    try { startActivity(Intent(Intent.ACTION_VIEW, u)) } catch (e: Exception) {}
                }
                return true
            }

            override fun onReceivedError(v: WebView?, r: WebResourceRequest?, e: WebResourceError?) {
                if (r != null && r.isForMainFrame && v != null && !(v.url ?: "").startsWith("file:")) {
                    v.loadUrl("file:///android_asset/index.html")
                }
            }
        }

        w.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                if (request == null) return
                runOnUiThread { handleWebPerm(request) }
            }

            override fun onShowFileChooser(v: WebView?, cb: ValueCallback<Array<Uri>>?, p: FileChooserParams?): Boolean {
                if (cb == null || p == null) return false
                fileCb?.onReceiveValue(null)
                fileCb = cb
                return try {
                    startActivityForResult(p.createIntent(), RC_FILE)
                    true
                } catch (e: Exception) {
                    fileCb = null
                    false
                }
            }

            override fun onJsAlert(v: WebView?, url: String?, message: String?, r: JsResult?): Boolean {
                if (r == null) return false
                AlertDialog.Builder(this@MainActivity).setMessage(message)
                    .setPositiveButton("OK") { _, _ -> r.confirm() }
                    .setOnCancelListener { r.cancel() }.show()
                return true
            }

            override fun onJsConfirm(v: WebView?, url: String?, message: String?, r: JsResult?): Boolean {
                if (r == null) return false
                AlertDialog.Builder(this@MainActivity).setMessage(message)
                    .setPositiveButton("OK") { _, _ -> r.confirm() }
                    .setNegativeButton("Bekor") { _, _ -> r.cancel() }
                    .setOnCancelListener { r.cancel() }.show()
                return true
            }

            override fun onJsPrompt(v: WebView?, url: String?, message: String?, def: String?, r: JsPromptResult?): Boolean {
                if (r == null) return false
                val et = EditText(this@MainActivity)
                et.setText(def ?: "")
                AlertDialog.Builder(this@MainActivity).setMessage(message).setView(et)
                    .setPositiveButton("OK") { _, _ -> r.confirm(et.text.toString()) }
                    .setNegativeButton("Bekor") { _, _ -> r.cancel() }
                    .setOnCancelListener { r.cancel() }.show()
                return true
            }
        }

        w.loadUrl(URL)
    }

    override fun onResume() {
        super.onResume()
        val w = web ?: return
        if ((w.url ?: "").startsWith("file:") && online()) w.loadUrl(URL)
    }

    override fun onActivityResult(rc: Int, res: Int, data: Intent?) {
        super.onActivityResult(rc, res, data)
        if (rc == RC_FILE) {
            fileCb?.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(res, data))
            fileCb = null
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        val w = web
        if (w != null && w.canGoBack()) w.goBack() else super.onBackPressed()
    }
}
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


def pick(patterns, exact):
    if os.path.exists(exact):
        return exact
    for p in patterns:
        m = sorted(glob.glob(p))
        if m:
            return m[0]
    return None


def main():
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    for p, c in F.items():
        write(p, c)

    icon_dir = os.path.join(ROOT, 'app/src/main/res/mipmap-xxxhdpi')
    os.makedirs(icon_dir, exist_ok=True)
    with open(os.path.join(icon_dir, 'ic_launcher.png'), 'wb') as f:
        f.write(base64.b64decode(''.join(ICON_B64.split())))

    html = pick(['index*.html'], 'index.html')
    if not html:
        sys.exit('XATO: index.html topilmadi')
    os.makedirs(os.path.join(ROOT, 'app/src/main/assets'), exist_ok=True)
    shutil.copy(html, os.path.join(ROOT, 'app/src/main/assets/index.html'))

    ks = pick(['nanogram*.keystore', 'edi*.keystore'], 'nanogram.keystore')
    if ks:
        shutil.copy(ks, os.path.join(ROOT, 'nanogram.keystore'))
        print('Keystore:', ks)
    else:
        print('OGOHLANTIRISH: keystore yoq, debug kalit ishlatiladi (yangilash uchun eski ilovani ochirish kerak boladi)')
    print('Tayyor:', len(F), 'fayl +', html)


if __name__ == '__main__':
    main()
    import add_push
    add_push.run()
