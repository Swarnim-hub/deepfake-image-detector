import React from 'react';
import { AlertTriangle, CheckCircle2, RefreshCw, Clock } from 'lucide-react';
import { ConfidenceMeter } from './ConfidenceMeter';
import { HeatmapView } from './HeatmapView';

export const ResultCard = ({ result, previewUrl, onReset }) => {
  if (!result) return null;

  const isFake = result.prediction === 'FAKE';

  return (
    <div className="w-full bg-slate-850/80 backdrop-blur-md rounded-2xl border border-slate-700/80 p-6 sm:p-8 shadow-2xl transition-all">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        
        {/* Left: Verdict and Details */}
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-2xl border ${
            isFake
              ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
              : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
          }`}>
            {isFake ? <AlertTriangle className="w-8 h-8" /> : <CheckCircle2 className="w-8 h-8" />}
          </div>

          <div>
            <div className="flex items-center gap-3">
              <span className={`text-2xl sm:text-3xl font-black tracking-wide ${
                isFake ? 'text-rose-400' : 'text-emerald-400'
              }`}>
                {isFake ? 'DEEPFAKE DETECTED' : 'LIKELY AUTHENTIC'}
              </span>
            </div>

            <p className="text-sm text-slate-300 mt-1 max-w-md">
              {isFake
                ? 'High likelihood of neural synthesis or facial tampering artifacts detected.'
                : 'No significant digital manipulation or synthetic artifact signatures detected.'}
            </p>

            <div className="flex flex-wrap items-center gap-4 mt-3 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                {result.processing_time_ms} ms
              </span>
              <span>•</span>
              <span>Model: EfficientNet-B0</span>
            </div>
          </div>
        </div>

        {/* Right: Confidence Gauge */}
        <div className="flex-shrink-0">
          <ConfidenceMeter value={result.confidence} isFake={isFake} />
        </div>
      </div>

      {/* Heatmap Interpretability Section */}
      <HeatmapView originalUrl={previewUrl} heatmapBase64={result.heatmap_base64} />

      {/* Reset / Try Another */}
      <div className="mt-8 flex justify-center">
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-sm font-semibold transition-all hover:scale-[1.02]"
        >
          <RefreshCw className="w-4 h-4" />
          Analyze Another Image
        </button>
      </div>
    </div>
  );
};
