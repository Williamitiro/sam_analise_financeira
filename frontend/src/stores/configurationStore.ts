// frontend/src/stores/configurationStore.ts
import { create } from 'zustand';
import { ProjecaoRequest } from '@/types/api.types';
import { defaultConfig } from '@/lib/api/projection';

interface ConfigurationState {
  config: ProjecaoRequest;
  setConfig: (newConfig: Partial<ProjecaoRequest>) => void;
  resetConfig: () => void;
}

export const useConfigurationStore = create<ConfigurationState>((set) => ({
  config: defaultConfig,
  setConfig: (newConfig) =>
    set((state) => ({
      config: { ...state.config, ...newConfig },
    })),
  resetConfig: () => set({ config: defaultConfig }),
}));
