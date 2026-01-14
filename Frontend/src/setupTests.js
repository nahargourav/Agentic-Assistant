// Import testing utilities
import '@testing-library/jest-dom'; // Provides custom matchers for testing DOM nodes

// Mocks MatchMedia (used for theme detection in some browsers)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query) => ({
    matches: query === '(prefers-color-scheme: dark)', // Default to dark mode for testing
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated method
    removeListener: jest.fn(), // Deprecated method
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  }),
});

// Mock localStorage for testing
Storage.prototype.getItem = jest.fn();
Storage.prototype.setItem = jest.fn();
Storage.prototype.removeItem = jest.fn();