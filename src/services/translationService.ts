// Translation service for English to Urdu and vice versa
// This is a mock service that would be replaced with a real translation API in production

interface TranslationCache {
  [key: string]: {
    en: string;
    ur: string;
    timestamp: number;
  };
}

class TranslationService {
  private cache: TranslationCache = {};
  private cacheExpiry = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  constructor() {
    // Initialize with some common translations
    this.cache = {
      'Welcome to our site': {
        en: 'Welcome to our site',
        ur: 'ہماری ویب سائٹ پر خوش آمدید',
        timestamp: Date.now()
      },
      'Start Learning': {
        en: 'Start Learning',
        ur: 'سیکھنا شروع کریں',
        timestamp: Date.now()
      },
      'View Modules': {
        en: 'View Modules',
        ur: 'ماڈیولز دیکھیں',
        timestamp: Date.now()
      },
      'Physical AI Principles': {
        en: 'Physical AI Principles',
        ur: 'فزیکل ای آئی کے اصول',
        timestamp: Date.now()
      },
      'Simulation Environments': {
        en: 'Simulation Environments',
        ur: 'Simulation Environments', // Keeping this in English as it's a technical term
        timestamp: Date.now()
      },
      'AI Integration': {
        en: 'AI Integration',
        ur: 'AI Integration', // Keeping this in English as it's a technical term
        timestamp: Date.now()
      },
      'Course': {
        en: 'Course',
        ur: 'کورس',
        timestamp: Date.now()
      },
      'Modules': {
        en: 'Modules',
        ur: 'ماڈیولز',
        timestamp: Date.now()
      },
      'GitHub': {
        en: 'GitHub',
        ur: 'GitHub',
        timestamp: Date.now()
      },
      'More': {
        en: 'More',
        ur: 'مزید',
        timestamp: Date.now()
      },
      'Resources': {
        en: 'Resources',
        ur: 'وسائل',
        timestamp: Date.now()
      },
    };
  }

  // Check if translation is in cache and not expired
  private isCached(text: string, targetLang: string): boolean {
    const cached = this.cache[text];
    if (!cached) return false;

    const isExpired = Date.now() - cached.timestamp > this.cacheExpiry;
    return !isExpired;
  }

  // Get translation from cache
  private getCachedTranslation(text: string, targetLang: string): string | null {
    if (!this.isCached(text, targetLang)) return null;

    return targetLang === 'ur' ? this.cache[text].ur : this.cache[text].en;
  }

  // Add translation to cache
  private setCache(text: string, en: string, ur: string): void {
    this.cache[text] = {
      en,
      ur,
      timestamp: Date.now()
    };
  }

  // Mock translation function - in a real app, this would call a translation API
  private async mockTranslate(text: string, targetLang: string): Promise<string> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 100));

    // For now, return the original text if no cached translation exists
    // In a real implementation, this would call an actual translation API
    return text;
  }

  // Main translation method
  async translate(text: string, targetLang: 'en' | 'ur'): Promise<string> {
    // Check if translation is already cached
    const cached = this.getCachedTranslation(text, targetLang);
    if (cached) {
      return cached;
    }

    // If not in cache, perform translation
    let translatedText: string;

    if (targetLang === 'ur') {
      // In a real implementation, this would call a translation API
      translatedText = await this.mockTranslate(text, targetLang);
      // Cache the result
      this.setCache(text, text, translatedText);
    } else {
      // If translating to English, return the original text
      translatedText = text;
      // Cache the result
      this.setCache(text, translatedText, text);
    }

    return translatedText;
  }

  // Batch translation method
  async translateBatch(texts: string[], targetLang: 'en' | 'ur'): Promise<string[]> {
    const results: string[] = [];

    for (const text of texts) {
      results.push(await this.translate(text, targetLang));
    }

    return results;
  }

  // Get current language direction (ltr or rtl)
  getDirection(lang: 'en' | 'ur'): 'ltr' | 'rtl' {
    return lang === 'ur' ? 'rtl' : 'ltr';
  }
}

// Create a singleton instance
export const translationService = new TranslationService();

// Hook for React components
export const useTranslationService = () => {
  return translationService;
};