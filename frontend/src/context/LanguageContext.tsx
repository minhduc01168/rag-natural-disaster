import React, { createContext, useContext, useState } from 'react';
import { Language, translations } from '../i18n/translations';

interface LanguageContextType {
  lang: Language;
  setLang: (lang: Language) => void;
  t: (path: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lang, setLangState] = useState<Language>(() => {
    const saved = localStorage.getItem('terra_lang');
    return (saved === 'en' || saved === 'vi') ? saved : 'vi';
  });

  const setLang = (newLang: Language) => {
    setLangState(newLang);
    localStorage.setItem('terra_lang', newLang);
  };

  // Helper function to access nested translation keys like 'nav.home' or 'weather.currentTemp'
  const t = (path: string): string => {
    const keys = path.split('.');
    let current: any = translations[lang];
    for (const key of keys) {
      if (current && typeof current === 'object' && key in current) {
        current = current[key];
      } else {
        return path; // Fallback to key name if not found
      }
    }
    return typeof current === 'string' ? current : path;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
