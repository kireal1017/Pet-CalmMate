import React from 'react';
import { View } from 'react-native';
import { WebView } from 'react-native-webview';

const htmlContent = `
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <style>
    body, html { margin:0; padding:0; height:100%; width:100%; background:#000; }
    video { width:100vw; height:100vh; }
  </style>
</head>
<body>
  <video id="video" controls autoplay></video>
  <script>
    var video = document.getElementById('video');
    var videoSrc = 'http://54.180.212.150:8080/hls/kvs-stream.m3u8';
    if (Hls.isSupported()) {
      var hls = new Hls();
      hls.loadSource(videoSrc);
      hls.attachMedia(video);
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = videoSrc;
    }
  </script>
</body>
</html>
`;

export default function HLSWebViewPlayer() {
  return (
    <View style={{ flex: 1, backgroundColor: 'black' }}>
      <WebView
        originWhitelist={['*']}
        source={{ html: htmlContent }}
        allowsInlineMediaPlayback
        mediaPlaybackRequiresUserAction={false}
        javaScriptEnabled
        domStorageEnabled
        style={{ flex: 1, backgroundColor: 'black' }}
      />
    </View>
  );
}
