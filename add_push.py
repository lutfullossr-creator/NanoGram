# NanoGram: push bildirishnoma (FCM) qo'shadi. make_apk.py yaratgan android/ papkasini o'zgartiradi.
import os, sys

# >>> Firebase Console -> Project settings -> Your apps -> Android -> "App ID" ni shu yerga yozing
APP_ID = "1:939214320261:android:957b426cfaf94ed55c6fec"
API_KEY = "AIzaSyAC_BJ5U8zfG8GA7yX8FmKu7GsmZnpjmfM"
PROJECT_ID = "tele-x-c5d7f"
SENDER_ID = "939214320261"

PKG = 'app/src/main/java/com/lutfullo/nanogram/'


def rd(root, p):
    return open(os.path.join(root, p), encoding='utf-8').read()


def wr(root, p, s):
    full = os.path.join(root, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(s)


def rep(s, old, new, name):
    if old not in s:
        sys.exit('add_push XATO: topilmadi -> ' + name)
    return s.replace(old, new, 1)


KT = r'''package com.lutfullo.nanogram

import android.app.Activity
import android.app.Application
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.webkit.JavascriptInterface
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import com.google.firebase.messaging.FirebaseMessaging
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

object NGPush {
    val history = HashMap<String, MutableList<String>>()

    fun init(c: Context) {
        try {
            if (FirebaseApp.getApps(c).isEmpty()) {
                FirebaseApp.initializeApp(
                    c,
                    FirebaseOptions.Builder()
                        .setApplicationId("__APP_ID__")
                        .setApiKey("__API_KEY__")
                        .setProjectId("__PROJECT_ID__")
                        .setGcmSenderId("__SENDER_ID__")
                        .build()
                )
            }
        } catch (e: Exception) {}
    }
}

class NGApp : Application() {
    override fun onCreate() {
        super.onCreate()
        NGPush.init(this)
    }
}

class NGBridge(private val a: Activity) {
    private var asked = false

    @JavascriptInterface
    fun getToken(): String {
        val p = a.getSharedPreferences("ng", 0)
        if (!asked) {
            asked = true
            try {
                FirebaseMessaging.getInstance().token.addOnSuccessListener {
                    p.edit().putString("fcm", it).apply()
                }
            } catch (e: Exception) {}
        }
        return p.getString("fcm", "") ?: ""
    }

    @JavascriptInterface
    fun requestNotifPermission() {
        if (Build.VERSION.SDK_INT >= 33 &&
            a.checkSelfPermission("android.permission.POST_NOTIFICATIONS") != PackageManager.PERMISSION_GRANTED) {
            a.runOnUiThread {
                a.requestPermissions(arrayOf("android.permission.POST_NOTIFICATIONS"), 9004)
            }
        }
    }
}

class NGService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        getSharedPreferences("ng", 0).edit().putString("fcm", token).apply()
    }

    override fun onMessageReceived(m: RemoteMessage) {
        if (MainActivity.inForeground) return
        val d = m.data
        val chatKey = d["chatKey"] ?: return
        val from = d["from"] ?: return
        val name = d["name"] ?: "NanoGram"
        val body = d["body"] ?: "Yangi xabar"

        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        nm.createNotificationChannel(
            NotificationChannel("messages", "Xabarlar", NotificationManager.IMPORTANCE_HIGH)
        )

        val list = NGPush.history.getOrPut(chatKey) { mutableListOf() }
        list.add(body)
        while (list.size > 5) list.removeAt(0)

        val launch = Intent(this, MainActivity::class.java)
        launch.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
        launch.putExtra("ng_from", from)
        val pi = PendingIntent.getActivity(
            this, chatKey.hashCode(), launch,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val inbox = Notification.InboxStyle()
        for (line in list) inbox.addLine(line)
        inbox.setBigContentTitle(name)

        val n = Notification.Builder(this, "messages")
            .setSmallIcon(R.drawable.ic_stat)
            .setContentTitle(name)
            .setContentText(body)
            .setStyle(inbox)
            .setNumber(list.size)
            .setContentIntent(pi)
            .setAutoCancel(true)
            .setGroup("ng_msgs")
            .setCategory(Notification.CATEGORY_MESSAGE)
            .build()
        nm.notify(chatKey.hashCode(), n)

        val summary = Notification.Builder(this, "messages")
            .setSmallIcon(R.drawable.ic_stat)
            .setGroup("ng_msgs")
            .setGroupSummary(true)
            .setAutoCancel(true)
            .build()
        nm.notify(0, summary)
    }
}
'''

ICON = '''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF"
        android:pathData="M20,2H4C2.9,2 2,2.9 2,4v18l4,-4h14c1.1,0 2,-0.9 2,-2V4C22,2.9 21.1,2 20,2z"/>
</vector>
'''


def run(root='android'):
    if 'XXXX' in APP_ID:
        print('add_push OGOHLANTIRISH: APP_ID yozilmagan, push qo\'shilmadi (APK oddiy quriladi)')
        return

    # 1) AndroidX (Firebase uchun majburiy)
    s = rd(root, 'gradle.properties')
    s = rep(s, 'android.useAndroidX=false', 'android.useAndroidX=true', 'gradle.properties')
    wr(root, 'gradle.properties', s)

    # 2) Firebase kutubxonasi
    s = rd(root, 'app/build.gradle.kts')
    s += '''
dependencies {
    implementation(platform("com.google.firebase:firebase-bom:33.1.0"))
    implementation("com.google.firebase:firebase-messaging")
}
'''
    wr(root, 'app/build.gradle.kts', s)

    # 3) Manifest
    p = 'app/src/main/AndroidManifest.xml'
    s = rd(root, p)
    s = rep(s, '<uses-permission android:name="android.permission.VIBRATE" />',
            '<uses-permission android:name="android.permission.VIBRATE" />\n'
            '    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />', p)
    s = rep(s, '<application\n        android:label="NanoGram"',
            '<application\n        android:name=".NGApp"\n        android:label="NanoGram"', p)
    s = rep(s, '    </application>',
            '        <service android:name=".NGService" android:exported="false">\n'
            '            <intent-filter>\n'
            '                <action android:name="com.google.firebase.MESSAGING_EVENT" />\n'
            '            </intent-filter>\n'
            '        </service>\n    </application>', p)
    wr(root, p, s)

    # 4) Kotlin + ikonka
    kt = (KT.replace('__APP_ID__', APP_ID).replace('__API_KEY__', API_KEY)
            .replace('__PROJECT_ID__', PROJECT_ID).replace('__SENDER_ID__', SENDER_ID))
    wr(root, PKG + 'NGPush.kt', kt)
    wr(root, 'app/src/main/res/drawable/ic_stat.xml', ICON)

    # 5) MainActivity
    p = PKG + 'MainActivity.kt'
    s = rd(root, p)
    s = rep(s, 'const val RC_WEBPERM = 9003',
            'const val RC_WEBPERM = 9003\n        @Volatile var inForeground = false', p)
    s = rep(s, '    override fun onResume() {\n        super.onResume()\n',
            '    override fun onPause() {\n        inForeground = false\n        super.onPause()\n    }\n\n'
            '    override fun onResume() {\n        super.onResume()\n'
            '        inForeground = true\n'
            '        try {\n'
            '            (getSystemService(Context.NOTIFICATION_SERVICE) as android.app.NotificationManager).cancelAll()\n'
            '            NGPush.history.clear()\n'
            '        } catch (e: Exception) {}\n', p)
    s = rep(s, '        w.loadUrl(URL)\n',
            '        w.addJavascriptInterface(NGBridge(this), "NGNative")\n'
            '        val from = intent?.getStringExtra("ng_from")\n'
            '        val q = if (from != null) "?open=" + Uri.encode("{\\"chat\\":true,\\"from\\":\\"" + from.replace("\\"", "") + "\\"}") else ""\n'
            '        w.loadUrl(URL + q)\n', p)
    s = rep(s, '    override fun onActivityResult(',
            '    override fun onNewIntent(i: Intent?) {\n'
            '        super.onNewIntent(i)\n'
            '        val f = i?.getStringExtra("ng_from") ?: return\n'
            '        web?.evaluateJavascript("window._ngOpen&&_ngOpen({chat:true,from:\'" + f.replace("\'", "") + "\'})", null)\n'
            '    }\n\n'
            '    override fun onActivityResult(', p)
    wr(root, p, s)
    print('add_push: push qo\'shildi')
