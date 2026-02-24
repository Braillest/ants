<script setup>
import { ref } from 'vue'
import DowntimeBanner from '@/components/banner/DowntimeBanner.vue'

const menuOpen = ref(false);

function toggleMenu() {
    menuOpen.value = !menuOpen.value
}

</script>

<template>
    <header>
        <DowntimeBanner />
        <nav>
            <a href="/">
                <div class="logo">
                    <img src="@/assets/braillest.png" alt="Logo">
                    Braillest
                </div>
            </a>
            <div class="right-bar">
                <!-- <div class="account">Login / Sign Up</div> -->
                <img src="@/assets/hamburger.png" alt="menu" @click="toggleMenu">
            </div>
        </nav>
        <div class="drawer-container" v-if="menuOpen">
            <div>
                <div class="drawer-header">About</div>
                <div>Approach</div>
                <div>Careers</div>
                <div>Commitment</div>
                <div>Mission</div>
                <div>Our Story</div>
                <div>Team</div>
            </div>
            <div>
                <div class="drawer-header">SL8</div>
                <div>Explorer</div>
                <div>Editor</div>
                <div>Publish</div>
                <div>Library</div>
                <div>Projects</div>
            </div>
            <div>
                <div class="drawer-header">Dashboard</div>
                <div>Orders</div>
                <div>Stats</div>
            </div>
            <div>
                <div class="drawer-header">Community</div>
                <div>Contact</div>
                <div>Discord</div>
                <div>GitHub</div>
                <div>Partners</div>
                <div>Forum</div>
            </div>
            <div>
                <div class="drawer-header">Learn</div>
                <div>What is Braille?</div>
                <div>Cost Analysis</div>
                <div>FAQ</div>
                <div>Getting Started</div>
                <div>How It Works</div>
                <div>SL8</div>
                <div>Tutorials</div>
            </div>
            <div>
                <div class="drawer-header">API</div>
                <div>Overview</div>
                <div>Documentation</div>
                <div>Installation</div>
                <div>Examples</div>
                <div>Changelog</div>
            </div>
            <div>
                <div class="drawer-header">News</div>
                <div>Blog</div>
                <div>Media Kit</div>
                <div>Press Releases</div>
                <div>Announcements</div>
            </div>
            <div>
                <div class="drawer-header">Support</div>
                <div>Contact Us</div>
                <div>Feedback</div>
                <div>Help Center</div>
                <div>Requests</div>
                <div>System Status</div>
            </div>
        </div>
    </header>
</template>

<style scoped>
    header {
        width: 100%;
        position: sticky;
        top: 0;
    }

    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        background-color: #3498db;
        border-bottom: 10px solid #2980b9;
        color: #fff;
        font-weight: bold;
        font-size: 42px;
    }

    @media (max-width: 480px) {
        nav {
            font-size: 24px;
        }
    }

    nav > a {
        text-decoration: none;
        color: #fff;
    }

    .logo {
        display: flex;
        align-items: center;
        padding: 20px;
        cursor: pointer;
    }

    .logo:hover {
        text-decoration: underline;
        background-color: #2980b9;
    }

    .logo img {
        width: 50px;
        height: 50px;
        margin-right: 20px;
    }

    .right-bar {
        display: flex;
        align-items: center;
    }

    .account {
        font-size: 24px;
        margin-right: 20px;
    }

    .right-bar img {
        width: 50px;
        height: 50px;
        padding: 20px;
        cursor: pointer;
    }

    .right-bar img:hover {
        background-color: #2980b9;
    }

    .drawer-container {
        background-color: #34495e;
        border-bottom: 10px solid #2c3e50;
        color: #fff;
        font-size: 24px;
        display: flex;
        justify-content: space-between;
        padding: 20px;
        flex-wrap: wrap;
        overflow-y: auto;
        max-height: calc(100vh - 190px);
    }

    .drawer-container > div {
        padding: 20px;
        width: calc(12.5% - 40px);
    }

    @media (max-width: 2040px) {
        .drawer-container > div {
            width: calc(25% - 40px);
        }
    }

    @media (max-width: 1440px) {
        .drawer-container > div {
            width: calc(33% - 40px);
        }
    }

    @media (max-width: 960px) {
        .drawer-container > div {
            width: calc(50% - 40px);
        }
    }

    @media (max-width: 480px) {
        .drawer-container > div {
            width: calc(100% - 40px);
        }
    }

    .drawer-container > div:hover {
        background-color: #2c3e50;
    }

    .drawer-container > div > div:hover {
        cursor: pointer;
        text-decoration: underline;
    }

    .drawer-header {
        font-weight: bold;
        text-decoration: underline;
        margin-bottom: 10px;
    }
</style>
