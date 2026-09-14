import React, { useState } from 'react';
import { Eye, Layers } from 'lucide-react';

export const HeatmapView = ({ originalUrl, heatmapBase64 }) => {
  const [viewMode, setViewMode] = useState('heatmap'); // 'heatmap' or 'original'

  if (!heatmapBase64) return null;

  return (
    <div className="mt-6 border-t border-slate-800 pt-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          <h4 className="font-semibold text-sm text-slate-200">Grad-CAM Interpretability Heatmap</h4>
        </div>

        <div className="flex bg-slate-800 p-1 rounded-lg border border-slate-700">
          <button
            onClick={() => setViewMode('original')}
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
              viewMode === 'original' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setViewMode('heatmap')}
            className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
              viewMode === 'heatmap' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Heatmap Overlay
          </button>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
        <div className="relative max-w-sm rounded-lg overflow-hidden border border-slate-700">
          <img
            src={viewMode === 'heatmap' ? heatmapBase64 : originalUrl}
            alt="Analysis target"
            className="w-full h-auto object-cover max-h-72"
          />
        </div>
      </div>

      <p className="text-xs text-slate-400 mt-2 text-center">
        Warmer areas (red/yellow) indicate facial features that most heavily influenced the AI decision.
      </p>
    </div>
  );
};
