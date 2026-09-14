import React, { useState } from 'react';
import { Header } from './components/Header';
import { UploadZone } from './components/UploadZone';
import { ResultCard } from './components/ResultCard';
import { detectImage } from './services/api';
import { Sparkles, ShieldCheck, Zap, Lock } from 'lucide-react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelected = async (file) => {
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError(null);
    setLoading(true);

    try {
      const data = await detectImage(file);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        'Failed to connect to the detection engine. If using the free cloud tier, the instance may take ~30s to spin up. Please retry.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      <Header />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-8 sm:py-12 flex flex-col items-center">
        
        {/* Hero Section */}
        <div className="text-center max-w-2xl mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>EfficientNet-B0 + Grad-CAM Explainability</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Verify Image Authenticity in Seconds
          </h2>
          <p className="text-slate-400 text-sm sm:text-base mt-3">
            Detect AI-generated faces, deepfake alterations, and neural blend artifacts. Free to use for everyone with zero signup or tracking.
          </p>
        </div>

        {/* Upload or Result Zone */}
        <div className="w-full">
          {!result ? (
            <UploadZone onFileSelected={handleFileSelected} isLoading={loading} />
          ) : (
            <ResultCard result={result} previewUrl={previewUrl} onReset={handleReset} />
          )}

          {error && (
            <div className="mt-4 p-4 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300 text-sm">
              <p className="font-semibold">Detection Notice</p>
              <p className="mt-1 text-xs">{error}</p>
            </div>
          )}
        </div>

        {/* How It Works & Privacy Badges */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full mt-16">
          <div className="p-5 rounded-2xl bg-slate-800/40 border border-slate-800 flex flex-col items-start">
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-3">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-sm text-slate-200">Instant Free Inference</h3>
            <p className="text-xs text-slate-400 mt-1">
              Optimized lightweight model provides swift classification without bloated enterprise cloud fees.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-800/40 border border-slate-800 flex flex-col items-start">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-3">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-sm text-slate-200">Privacy First</h3>
            <p className="text-xs text-slate-400 mt-1">
              No database, no user accounts, and no persistent disk storage. Images are processed in RAM and discarded immediately.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-800/40 border border-slate-800 flex flex-col items-start">
            <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-3">
              <Lock className="w-5 h-5" />
            </div>
            <h3 className="font-semibold text-sm text-slate-200">Transparent AI</h3>
            <p className="text-xs text-slate-400 mt-1">
              Grad-CAM heatmaps highlight manipulated zones so you can see exactly why an image was deemed authentic or synthetic.
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        <p>Deepfake Image Detector • Built for public, accessible digital authenticity verification.</p>
      </footer>
    </div>
  );
}

export default App;
