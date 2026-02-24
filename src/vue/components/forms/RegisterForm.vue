<script setup>
import { ref } from 'vue';
import BaseInput from '../input/BaseInput.vue';

const email = ref('');
const password = ref('');

const handleRegister = () => {
  alert(`Registering with: \nEmail: ${email.value} \nPassword: ${password.value}`);
};
</script>

<template>

<form @submit.prevent="handleRegister" class="register-card">
    <h2>Create Account</h2>

    <BaseInput v-model="email" label="Email Address" type="email" />
    <BaseInput v-model="password" label="Password" type="password" />

    <button type="submit" :disabled="!email || !password">
      register
    </button>

    <p class="debug">Current State: {{ { email, password } }}</p>
  </form>
</template>

<style scoped>
.register-card { max-width: 300px; padding: 2rem; border: 1px solid #eee; border-radius: 8px; }
button { width: 100%; padding: 10px; background: #42b883; color: white; border: none; cursor: pointer; }
button:disabled { background: #ccc; }
.debug { font-size: 0.8rem; color: #666; margin-top: 1rem; }
</style>
