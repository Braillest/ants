<template>
  <div>
    <h1>Results</h1>
    <pre>{{ result }}</pre>

    <router-link to="/">Start Over</router-link>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const result = history.state?.result || { error: 'No result found' }
</script>
