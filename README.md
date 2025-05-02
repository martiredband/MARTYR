<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Mastering Engine Overview</title>
  <style>
    * {
      box-sizing: border-box;
    }

    html, body {
      background-color: #000;
      color: #fff;
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 0;
    }

    body {
      padding: 6rem 2rem;
    }

    .container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 0 1rem;
    }

    .shadow {
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9); /* fuerte sombra negra */
    }

    .download-button {
      display: block;
      margin: 3rem auto 2rem;
      background-color: #1a1a1a;
      color: orange;
      padding: 1rem 2rem;
      border: none;
      border-radius: 10px;
      font-size: 1.1rem;
      font-weight: bold;
      text-align: center;
      text-decoration: none;
      width: max-content;
      transition: background-color 0.3s ease;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9);
    }

    .download-button:hover {
      background-color: #222;
    }

    .grid-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 2rem;
      margin-bottom: 3rem;
    }

    .card {
      background-color: #1a1a1a;
      padding: 1.5rem;
      border-radius: 12px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9);
      transition: background-color 0.3s ease;
    }

    .card:hover {
      background-color: #222;
    }

    .card h2 {
      font-size: 1.2rem;
      margin-bottom: 0.8rem;
      color: #fff;
    }

    .card p {
      font-size: 0.95rem;
      line-height: 1.5;
      color: #ccc;
    }

    .section {
      background-color: #1a1a1a;
      padding: 2rem;
      border-radius: 12px;
      margin-bottom: 2rem;
      overflow-x: auto;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9);
    }

    .section h3 {
      color: #fff;
      margin-top: 0;
    }

    .section p,
    .section ul {
      color: #ccc;
      font-size: 0.95rem;
    }

    .section code,
    .section pre {
      background-color: #222;
      padding: 0.5rem;
      border-radius: 6px;
      color: #ffcc00;
      font-family: Consolas, monospace;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-x: auto;
      display: block;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.8);
    }

    a {
      color: #ff4444;
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <div class="container">

    <a class="download-button shadow" href="https://martired.com/martyr-downloads/" target="_blank">Download</a>

    <div class="grid-container">
      <div class="card shadow">
        <h2>Machine Learning Core</h2>
        <p>
          Trained on thousands of professionally mixed songs from well-known bands, allowing the system to learn tonal balance, dynamics, and spatial characteristics of expert mastering.
        </p>
      </div>
      <div class="card shadow">
        <h2>Precision Algorithms</h2>
        <p>
          Processes billions of spectral operations per track. This enables deep, nonlinear analysis and sophisticated enhancements that go far beyond the constraints of real-time DSP.
        </p>
      </div>
      <div class="card shadow">
        <h2>Automated Decision System</h2>
        <p>
          The engine listens and adapts. It mimics the workflow of professional engineers by adjusting parameters in real-time to suit the input's unique profile.
        </p>
      </div>
      <div class="card shadow">
        <h2>Local Processing</h2>
        <p>
          All processing is done offline on your machine—ensuring privacy, speed, and full hardware utilization without cloud reliance.
        </p>
      </div>
    </div>

    <div class="section shadow">
      <h3>Technology Behind the App</h3>
      <p>
        This mastering tool is built entirely in <strong>Python</strong> using the open-source engine
        <a href="https://github.com/sergree/matchering" target="_blank">Matchering</a>, which is available here:
        <a href="https://github.com/sergree/matchering/releases" target="_blank">https://github.com/sergree/matchering/releases</a>.
        It replicates the reference mastering technique: matching the sound of a target track to a professionally mastered reference.
      </p>
      <ul>
        <li>Algorithm trained on expertly mixed and mastered songs.</li>
        <li>Smart matching of dynamic range, stereo width, and loudness.</li>
        <li>Realistic emulation of analog mastering chains.</li>
      </ul>
    </div>

    <div class="section shadow">
      <h3>Installation & Package Content</h3>
      <p>
        The application is <strong>under development</strong>. A downloadable package is available and includes:
      </p>
      <ul>
        <li><code>MARTYR.exe</code> – Windows executable</li>
        <li><code>MARTYR.py</code> – Python source code</li>
      </ul>
      <p>
        More updates and support for other systems will be added soon. The app works entirely with Python.
      </p>
      <p>
        To run in Python, install the following dependencies:
      </p>
      <pre><code>pip install matchering==2.1.6 pandas numpy soundfile matplotlib imageio-ffmpeg requests</code></pre>
    </div>

  </div>

</body>
</html>
