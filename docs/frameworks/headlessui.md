# Headless UI (Vue) 使用指南

## 元信息
- 官网：https://headlessui.com/vue
- 包名：`@headlessui/vue`
- 版本：v1.7+
- 语言：Vue 3
- 特点：完全无样式、无障碍支持、Composition API

## 安装

```bash
npm install @headlessui/vue
```

## 常用组件速查

### Dialog 对话框

**基础用法：**
```vue
<script setup>
import { ref } from 'vue'
import { Dialog, DialogPanel, DialogTitle, DialogDescription } from '@headlessui/vue'

const isOpen = ref(true)
</script>

<template>
  <Dialog :open="isOpen" @close="isOpen = false" class="relative z-50">
    <!-- 背景遮罩 -->
    <div class="fixed inset-0 bg-black/30" aria-hidden="true" />

    <!-- 对话框内容 -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel class="w-full max-w-md rounded bg-white p-6">
        <DialogTitle class="text-lg font-bold">对话框标题</DialogTitle>
        <DialogDescription class="mt-2 text-gray-600">
          对话框描述内容
        </DialogDescription>

        <div class="mt-4 flex gap-2">
          <button @click="isOpen = false">取消</button>
          <button @click="isOpen = false">确认</button>
        </div>
      </DialogPanel>
    </div>
  </Dialog>
</template>
```

**Props：**
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| open | boolean | - | 控制显示/隐藏（必填） |
| as | string | 'div' | 渲染的元素标签 |
| static | boolean | false | 是否禁用过渡动画 |
| unmount | boolean | true | 关闭时是否卸载组件 |

**Events：**
| 事件 | 参数 | 说明 |
|------|------|------|
| close | - | 用户尝试关闭时触发（按 ESC 或点击遮罩） |

**子组件：**
- `DialogPanel` - 对话框内容容器
- `DialogTitle` - 标题（自动设置 aria-labelledby）
- `DialogDescription` - 描述（自动设置 aria-describedby）
- `DialogOverlay` - 遮罩层（可选）

---

### Menu 下拉菜单

**基础用法：**
```vue
<script setup>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
</script>

<template>
  <Menu as="div" class="relative">
    <MenuButton class="px-4 py-2 bg-blue-500 text-white rounded">
      选项
    </MenuButton>

    <MenuItems class="absolute right-0 mt-2 w-48 bg-white rounded shadow-lg">
      <MenuItem v-slot="{ active }">
        <a href="#" :class="{ 'bg-blue-100': active }" class="block px-4 py-2">
          编辑
        </a>
      </MenuItem>
      <MenuItem v-slot="{ active }">
        <a href="#" :class="{ 'bg-blue-100': active }" class="block px-4 py-2">
          删除
        </a>
      </MenuItem>
    </MenuItems>
  </Menu>
</template>
```

**Props（Menu）：**
| 属性 | 类型 | 说明 |
|------|------|------|
| as | string | 默认 'div' |

**MenuItem 作用域插槽：**
| 属性 | 类型 | 说明 |
|------|------|------|
| active | boolean | 是否高亮（键盘导航时） |
| disabled | boolean | 是否禁用 |

---

### Listbox 选择器（替代 Select）

**基础用法：**
```vue
<script setup>
import { ref } from 'vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'

const people = [
  { id: 1, name: 'Tom Cook' },
  { id: 2, name: 'Wade Cooper' },
]
const selectedPerson = ref(people[0])
</script>

<template>
  <Listbox v-model="selectedPerson">
    <div class="relative">
      <ListboxButton class="w-full px-4 py-2 border rounded text-left">
        {{ selectedPerson.name }}
      </ListboxButton>

      <ListboxOptions class="absolute w-full mt-1 bg-white shadow-lg rounded">
        <ListboxOption
          v-for="person in people"
          :key="person.id"
          :value="person"
          v-slot="{ selected, active }"
        >
          <div :class="{ 'bg-blue-100': active }" class="px-4 py-2">
            <span :class="{ 'font-bold': selected }">{{ person.name }}</span>
          </div>
        </ListboxOption>
      </ListboxOptions>
    </div>
  </Listbox>
</template>
```

**Props（Listbox）：**
| 属性 | 类型 | 说明 |
|------|------|------|
| modelValue | any | 当前选中值（v-model） |
| by | string/function | 比较键值的方式 |
| multiple | boolean | 是否多选 |
| disabled | boolean | 是否禁用 |

**ListboxOption 作用域插槽：**
| 属性 | 类型 | 说明 |
|------|------|------|
| selected | boolean | 是否选中 |
| active | boolean | 是否高亮 |
| disabled | boolean | 是否禁用 |

---

### Combobox 可搜索选择器

**基础用法：**
```vue
<script setup>
import { ref, computed } from 'vue'
import { Combobox, ComboboxInput, ComboboxOptions, ComboboxOption } from '@headlessui/vue'

const people = ['Tom Cook', 'Wade Cooper', 'Tanya Fox']
const query = ref('')
const selectedPerson = ref('')

const filteredPeople = computed(() =>
  query.value === ''
    ? people
    : people.filter(person => person.toLowerCase().includes(query.value.toLowerCase()))
)
</script>

<template>
  <Combobox v-model="selectedPerson">
    <div class="relative">
      <ComboboxInput
        @change="query = $event.target.value"
        :displayValue="person => person"
        class="w-full px-4 py-2 border rounded"
      />

      <ComboboxOptions class="absolute w-full mt-1 bg-white shadow-lg rounded">
        <ComboboxOption
          v-for="person in filteredPeople"
          :key="person"
          :value="person"
          v-slot="{ selected, active }"
        >
          <div :class="{ 'bg-blue-100': active }" class="px-4 py-2">
            {{ person }}
          </div>
        </ComboboxOption>
      </ComboboxOptions>
    </div>
  </Combobox>
</template>
```

**Props（Combobox）：**
| 属性 | 类型 | 说明 |
|------|------|------|
| modelValue | any | 当前值 |
| by | string/function | 比较方式 |

---

### Disclosure 展开/折叠

**基础用法：**
```vue
<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
</script>

<template>
  <Disclosure>
    <DisclosureButton class="px-4 py-2 bg-gray-100 rounded">
      点击展开
    </DisclosureButton>
    <DisclosurePanel class="px-4 py-2">
      隐藏的内容
    </DisclosurePanel>
  </Disclosure>
</template>
```

---

### Popover 弹出层

**基础用法：**
```vue
<script setup>
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
</script>

<template>
  <Popover class="relative">
    <PopoverButton class="px-4 py-2 bg-blue-500 text-white rounded">
      打开弹出层
    </PopoverButton>

    <PopoverPanel class="absolute z-10 p-4 bg-white shadow-lg rounded">
      弹出内容
    </PopoverPanel>
  </Popover>
</template>
```

---

### Transition 过渡动画

**基础用法：**
```vue
<script setup>
import { TransitionRoot, TransitionChild } from '@headlessui/vue'
import { ref } from 'vue'

const isShowing = ref(false)
</script>

<template>
  <button @click="isShowing = !isShowing">切换</button>

  <TransitionRoot
    :show="isShowing"
    enter="transition-opacity duration-300"
    enter-from="opacity-0"
    enter-to="opacity-100"
    leave="transition-opacity duration-200"
    leave-from="opacity-100"
    leave-to="opacity-0"
  >
    <div class="p-4 bg-blue-500 text-white">
      带过渡的内容
    </div>
  </TransitionRoot>
</template>
```

**过渡类名：**
| 阶段 | 类名 | 说明 |
|------|------|------|
| enter | 过渡开始前的类名 | 如 `opacity-0` |
| enter-from | 进入动画起始状态 | |
| enter-to | 进入动画结束状态 | 如 `opacity-100` |
| leave | 离开动画配置 | 如 `transition-opacity duration-200` |
| leave-from | 离开动画起始状态 | |
| leave-to | 离开动画结束状态 | |

---

### Radio Group 单选组

**基础用法：**
```vue
<script setup>
import { ref } from 'vue'
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'

const plans = ['Startup', 'Business', 'Enterprise']
const selectedPlan = ref(plans[0])
</script>

<template>
  <RadioGroup v-model="selectedPlan">
    <RadioGroupLabel>选择计划</RadioGroupLabel>
    <RadioGroupOption
      v-for="plan in plans"
      :key="plan"
      :value="plan"
      v-slot="{ checked, active }"
    >
      <div :class="{ 'bg-blue-500 text-white': checked, 'ring-2 ring-blue-500': active }">
        {{ plan }}
      </div>
    </RadioGroupOption>
  </RadioGroup>
</template>
```

---

### Switch 开关

**基础用法：**
```vue
<script setup>
import { ref } from 'vue'
import { Switch, SwitchLabel } from '@headlessui/vue'

const enabled = ref(false)
</script>

<template>
  <SwitchGroup>
    <div class="flex items-center">
      <SwitchLabel class="mr-4">启用功能</SwitchLabel>
      <Switch
        v-model="enabled"
        :class="enabled ? 'bg-blue-600' : 'bg-gray-200'"
        class="relative inline-flex h-6 w-11 rounded-full transition"
      >
        <span
          :class="enabled ? 'translate-x-6' : 'translate-x-1'"
          class="inline-block h-4 w-4 transform rounded-full bg-white transition"
        />
      </Switch>
    </div>
  </SwitchGroup>
</template>
```

---

### Tabs 标签页

**基础用法：**
```vue
<script setup>
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
</script>

<template>
  <TabGroup>
    <TabList class="flex gap-4">
      <Tab v-slot="{ selected }">
        <button :class="{ 'border-b-2 border-blue-500': selected }">Tab 1</button>
      </Tab>
      <Tab v-slot="{ selected }">
        <button :class="{ 'border-b-2 border-blue-500': selected }">Tab 2</button>
      </Tab>
    </TabList>

    <TabPanels class="mt-4">
      <TabPanel>内容 1</TabPanel>
      <TabPanel>内容 2</TabPanel>
    </TabPanels>
  </TabGroup>
</template>
```

---

## 最佳实践

### 1. 始终处理无障碍属性
Headless UI 自动处理 aria 属性，但你需要确保：
- Dialog 有 DialogTitle
- Menu 的 MenuButton 有明确的文本

### 2. 样式建议
- 使用 Tailwind CSS（推荐）
- 所有组件都是无样式的，完全由你控制

### 3. 键盘导航
- Dialog: ESC 关闭，Tab 在内部循环
- Menu: ↑↓ 导航，Enter/Space 选择，ESC 关闭
- Listbox: ↑↓ 导航，Enter 选择

### 4. 常见组合
```vue
<!-- Dialog + Transition -->
<TransitionRoot appear :show="isOpen">
  <Dialog @close="isOpen = false">
    <TransitionChild>
      <div class="fixed inset-0 bg-black/30" />
    </TransitionChild>
    <TransitionChild>
      <DialogPanel>...</DialogPanel>
    </TransitionChild>
  </Dialog>
</TransitionRoot>
```

---

## 注意事项

1. **Vue 版本要求**：Vue 3.0+
2. **样式完全由你控制**：组件只提供行为和结构
3. **默认使用 renderless pattern**：通过 v-slot 获取状态
4. **过渡动画需要配合 Transition 组件**：原生 Dialog/Menu 等没有内置动画

---

## 更新记录

- 2024-02-21: 创建文档，包含 10+ 常用组件
