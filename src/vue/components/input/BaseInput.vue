<script setup>
// defineModel makes 'modelValue' accessible as a local ref
const model = defineModel();

defineProps({
  label: String,
  type: { type: String, default: 'text' },
});
</script>

<template>
  <div class="input-group">
    <label>{{ label }}</label>
    <input
      :type="type" 
      v-model="model" 
      placeholder="Type here..."
    />
  </div>
</template>

<style scoped>
.input-group { margin-bottom: 1rem; display: flex; flex-direction: column; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
</style>
