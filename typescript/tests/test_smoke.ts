import { describe, it, expect } from 'vitest';
import { greet } from '../src/[name]/index';

describe('greet', () => {
  it('returns a greeting', () => {
    expect(greet('world')).toBe('Hello, world!');
  });
});
