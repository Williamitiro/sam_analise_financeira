import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utilitário para merge de classes Tailwind
 * Combina clsx + tailwind-merge para evitar conflitos de classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
