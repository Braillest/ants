<template>
    <footer class="site-footer">
        <div class="footer-content">
            <div class="footer-section brand">
                <h3>⠠⠃⠗⠇⠌</h3>
                <p>Democratizing braille.</p>
            </div>
            <div class="footer-section links">
                <h4>Quick Links</h4>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div>
            <div class="footer-section social">
                <h4>Connect</h4>
                <div class="social-icons">
                    <!-- Text placeholders for icons, normally would use SVG or icon font -->
                    <a href="#" aria-label="Facebook">FB</a>
                    <a href="#" aria-label="Twitter">TW</a>
                    <a href="#" aria-label="LinkedIn">LI</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&#127279; {{ new Date().getFullYear() }} Braillest. All rights reversed.</p>
        </div>
    </footer>
</template>

<style scoped>
.site-footer {
    background-color: #34495e; /* Darker shade for contrast */
    border-top: 10px solid #2c3e50;
    color: #ecf0f1;
    padding: 20px;
    font-family: sans-serif;
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: 0px auto;
    gap: 20px;
}

.footer-section {
    flex: 1;
    min-width: calc(33% - 40px);
}

@media (max-width: 960px) {
    .footer-section {
        min-width: calc(50% - 40px);
    }
}

@media (max-width: 480px) {
    .footer-section {
        min-width: calc(100% - 40px);
    }
}

.footer-section h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #ffffff;
}

.footer-section h4 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #ecf0f1;
    border-bottom: 2px solid #34495e;
    display: inline-block;
    padding-bottom: 0.25rem;
}

.footer-section p {
    line-height: 1.6;
    color: #bdc3c7;
}

.footer-section ul {
    list-style: none;
    padding: 0;
}

.footer-section ul li {
    margin-bottom: 0.5rem;
}

.footer-section a {
    color: #bdc3c7;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: #3498db;
}

.social-icons a {
    display: inline-block;
    margin-right: 1rem;
    font-weight: bold;
    padding: 0.5rem;
    background: #34495e;
    border-radius: 4px;
    min-width: 40px;
    text-align: center;
}

.social-icons a:hover {
    background: #3498db;
    color: #fff;
}

.footer-bottom {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #34495e;
    font-size: 0.9rem;
    color: #7f8c8d;
}
</style>

<script setup>
</script>
