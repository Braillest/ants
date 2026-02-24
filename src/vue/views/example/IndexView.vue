<template>
  <div>
    <h1>Submit Job</h1>

    <form @submit.prevent="handleSubmit">
      <input
        v-model="inputValue"
        placeholder="Enter value"
        required
      />
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { submitForm } from '../services/api'

const router = useRouter()
const inputValue = ref('')

async function handleSubmit() {
  const response = await submitForm({ value: inputValue.value })

  router.push({
    name: 'loading',
    query: { jobId: response.jobId }
  })
}
</script>
