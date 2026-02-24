<script setup>
import { ref } from 'vue';
import BaseInput from "../../components/input/BaseInput.vue";

const username = ref('');
const password = ref('');

function handleSubmit() {
    console.log('Login attempt:', username.value, password.value);
}
</script>

<template>
    <div>
        <h1>Login</h1>
    </div>
    <form action="/login" method="post" @submit.prevent="handleSubmit">
        <BaseInput v-model="username" label="username" type="text" />
        <BaseInput v-model="password" label="password" type="password" />
        <button type="submit">login</button>
    </form>
    <div>
        <a href="/forgot-password">Forgot your password?</a>
    </div>
    <div>
        <h1>Create Account</h1>
    </div>
    <form action="/register" method="post" @submit.prevent="handleSubmit">
        <BaseInput v-model="username" label="username" type="text" />
        <BaseInput v-model="password" label="password" type="password" />
        <button type="submit">create account</button>
    </form>
</template>
