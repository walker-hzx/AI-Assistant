/**
 * Global Teardown - Playwright 全局清理
 *
 * 在所有测试结束后执行，确保没有残留测试数据
 * 清理逻辑：
 * 1. 清理带有 test- 前缀的租户
 * 2. 清理带有 test- 前缀的用户
 * 3. 清理过期的测试数据（超过 24 小时）
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface CleanupResult {
  tenants: number;
  users: number;
  errors: string[];
}

async function globalTeardown() {
  console.log('\n🧹 开始全局清理...');

  const result: CleanupResult = {
    tenants: 0,
    users: 0,
    errors: [],
  };

  try {
    // 方案 1: 通过 API 清理（推荐）
    // 清理测试租户
    try {
      const tenantResponse = await fetch(
        `${process.env.BASE_URL || 'http://localhost:3000'}/api/tenants?prefix=test-`
      );
      if (tenantResponse.ok) {
        const tenants = await tenantResponse.json();
        for (const tenant of tenants.data || []) {
          await fetch(`${process.env.BASE_URL}/api/tenants/${tenant.id}`, {
            method: 'DELETE',
          });
          result.tenants++;
        }
      }
    } catch (e) {
      result.errors.push(`租户清理失败: ${e}`);
    }

    // 清理测试用户
    try {
      const userResponse = await fetch(
        `${process.env.BASE_URL || 'http://localhost:3000'}/api/users?prefix=test-`
      );
      if (userResponse.ok) {
        const users = await userResponse.json();
        for (const user of users.data || []) {
          await fetch(`${process.env.BASE_URL}/api/users/${user.id}`, {
            method: 'DELETE',
          });
          result.users++;
        }
      }
    } catch (e) {
      result.errors.push(`用户清理失败: ${e}`);
    }

    // 方案 2: 如果 API 不可用，尝试数据库清理（仅本地开发）
    if (process.env.NODE_ENV === 'development' && !process.env.CI) {
      try {
        await cleanupViaDatabase(result);
      } catch (e) {
        console.log('数据库清理跳过（非必要）');
      }
    }

    // 打印清理结果
    console.log('\n✅ 全局清理完成:');
    console.log(`   - 清理租户: ${result.tenants}`);
    console.log(`   - 清理用户: ${result.users}`);

    if (result.errors.length > 0) {
      console.log('\n⚠️ 清理中的错误:');
      result.errors.forEach((e) => console.log(`   - ${e}`));
    }
  } catch (error) {
    console.error('❌ 全局清理失败:', error);
    // teardown 失败不应导致测试失败，只是警告
  }
}

/**
 * 通过数据库直接清理（仅本地开发）
 */
async function cleanupViaDatabase(result: CleanupResult) {
  // 示例：使用 prisma 清理
  // const { PrismaClient } = require('@prisma/client');
  // const prisma = new PrismaClient();
  //
  // const tenants = await prisma.tenant.deleteMany({
  //   where: { name: { startsWith: 'test-' } },
  // });
  // result.tenants = tenants.count;
  //
  // await prisma.$disconnect();

  console.log('数据库清理需要根据实际 ORM 实现');
}

export default globalTeardown;
