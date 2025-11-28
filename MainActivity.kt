package com.cryptoprobot

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        btnAnalyze.setOnClickListener {
            val url = editApiUrl.text.toString().trim()
            if (url.isEmpty()) {
                txtOutput.text = "Enter API URL"
                return@setOnClickListener
            }
            txtOutput.text = "Waiting..."
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    val client = OkHttpClient()
                    val json = "{}".toRequestBody("application/json".toMediaTypeOrNull())
                    val req = Request.Builder().url(url).post(json).build()
                    val resp = client.newCall(req).execute()
                    val body = resp.body?.string() ?: "{}"
                    runOnUiThread { txtOutput.text = body }
                } catch (e: Exception) {
                    runOnUiThread { txtOutput.text = "Error: " + e.message }
                }
            }
        }
    }
}
