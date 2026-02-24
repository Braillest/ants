<script setup>
import { ref } from "vue"

const showBanner = ref(true)

const downtimeStart = "2026/2/2 12:00 PM CST"
const downtimeEnd = "2026/2/2 4:00 PM CST"
const start = new Date(downtimeStart)
const end = new Date(downtimeEnd)

const isBeforeDowntime = () => {
    const now = new Date()
    return now < start
}

const isAfterDowntime = () => {
    const now = new Date()
    return now > end
}

const bannerWasClosed = () => {
    return localStorage.getItem("downtimeBannerClosed")
}

const closeBanner = () => {
    localStorage.setItem("downtimeBannerClosed", true)
    showBanner.value = false
}

// Testing code left for reference.
// console.log(bannerWasClosed())
// localStorage.removeItem("downtimeBannerClosed")

// Remove the local storage item if it's past the end date.
if (isAfterDowntime()) {
    localStorage.removeItem("downtimeBannerClosed")
}

// Check if the banner should initialize as hidden.
if (bannerWasClosed() || !isBeforeDowntime()) {
    showBanner.value = false
}
</script>

<template>
    <div v-if="showBanner">
        Planned downtime from {{ downtimeStart }} to {{ downtimeEnd }}.
        <a @click="closeBanner">X</a>
    </div>
</template>

<style scoped>
    div {
        padding: 10px;
        text-align: center;
        background-color: #f1c40f;
        border-bottom: 10px solid #f39c12;
        color: #000;
        font-weight: bold;
        align-items: center;
        display: flex;
        justify-content: center;
        text-align: center;
        font-size: 24px;
    }

    a {
        background-color: #f39c12;
        color: #fff;
        padding: 10px;
        margin-left: 10px;
        text-decoration: none;
        cursor: pointer;
    }
</style>
