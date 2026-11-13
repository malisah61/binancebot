package com.malisah.kriptoanaliz;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        web.setBackgroundColor(0xFF0B0F14);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        // Yerel sayfanın Binance API'sine erişebilmesi için (CORS)
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient()); // confirm() pencereleri için
        web.loadUrl("file:///android_asset/www/index.html");
        setContentView(web);
    }

    @Override
    public void onBackPressed() {
        // Detay/Bot sekmesindeyken geri tuşu taramaya döner, taramadaysa uygulamadan çıkar
        web.evaluateJavascript("(function(){var s=document.getElementById('pScan');if(s.classList.contains('hide')){show('pScan');return 1}return 0})()",
            v -> { if ("0".equals(v)) MainActivity.super.onBackPressed(); });
    }
}
