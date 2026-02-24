<template>
  <div>
    <h1>Processing...</h1>
    <p>Please wait while we complete your request.</p>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { checkJobStatus } from '../services/api'

const route = useRoute()
const router = useRouter()
const jobId = route.query.jobId

let intervalId

async function poll() {
  const response = await checkJobStatus(jobId)

  if (response.status === 'complete') {
    clearInterval(intervalId)
    router.replace({
      name: 'results',
      state: { result: response.result }
    })
  }
}

onMounted(() => {
  intervalId = setInterval(poll, 2000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>
