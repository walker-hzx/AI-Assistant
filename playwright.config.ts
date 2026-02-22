import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // ========== Global Teardown ==========
  // 测试全部结束后执行清理，确保没有残留数据
  teardown: './tests/e2e/teardown.ts',
});

// 全局 teardown 会在以下时机执行：
// 1. 所有测试完成后
// 2. Ctrl+C 中断时
// 3. CI 管道结束时
