<script setup>

</script>

<template>
    <div class="container">
        <div id="flyers" class="photo">
            <h1>Braillest</h1>
        </div>
        <div class="divider"></div>
        <div id="flyers" class="caption vignette fill">
            <h6>"Use 3D printed molds to repeatably <span>emboss</span> braille."</h6>
        </div>
        <div class="divider"></div>
        <div class="caption">
            <h6 class="clear-shadow dark">Braillest believes in open-source and public domain.</h6>
        </div>
        <div class="divider"></div>
        <div class="caption">
            <h6 class="clear-shadow dark">And we're making our process more accessible by creating:</h6>
        </div>
        <div class="divider"></div>
        <div id="sl8" class="caption fill">
            <h6>SL8, a free, open-source, web-based braille editor.</h6>
        </div>
        <div class="caption">
            <h6 class="clear-shadow dark">Write custom workflows to:</h6>
        </div>
        <div class="divider"></div>
        <div id="transcribe" class="photo fill">
            <h1>Transcribe</h1>
        </div>
        <div class="divider"></div>
        <div id="format" class="photo fill">
            <h1>Format</h1>
        </div>
        <div class="divider"></div>
        <div id="paginate" class="photo fill">
            <h1>Paginate</h1>
        </div>
        <div class="divider"></div>
        <div id="mold-render" class="photo fill">
            <h1>Generate</h1>
        </div>
        <div class="divider"></div>
        <div id="negative-mold" class="photo fill">
            <h1>Print</h1>
        </div>
        <div class="divider"></div>
        <div id="mold-press" class="photo">
            <h1>Press</h1>
        </div>
        <div class="divider"></div>
        <div id="repair" class="photo">
            <h1>Repair</h1>
        </div>
        <div class="divider"></div>
        <div id="dashboard" class="caption fill">
            <h6>Watch braillest's processes create braille materials in real-time.</h6>
        </div>
        <div class="divider"></div>
        <div id="cost" class="caption">
            <h6 class="clear-shadow dark">A $1.00 mold is capable of creating thousands of copies.</h6>
        </div>
        <div class="divider"></div>
        <div id="mold-result" class="caption fill">
            <h6>We're leading the path towards individual braille ownership.</h6>
        </div>
        <div class="divider"></div>
        <div id="library" class="caption fill">
            <a href="https://github.com/orgs/Braillest-Books/repositories" target="_blank">
                <h6 class="clear-shadow dark">View our digital braille library.</h6>
            </a>
        </div>
        <div class="divider"></div>
        <div class="caption">
            <a href="/commitment">
                <h6 class="clear-shadow dark">Read our commitment to public domain and open source.</h6>
            </a>
        </div>
        <div class="divider"></div>
        <div class="caption">
            <h6 class="clear-shadow dark">Read our founder's story.</h6>
        </div>
        <div class="divider"></div>
        <div id="donate" class="caption donate-vignette">
            <h6 class="clear-shadow">Donate to support our mission.</h6>
        </div>
    </div>
</template>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        text-align: center;
        margin: 20px;
        border: 2px solid #333;
        background-color: #fff;
    }

    .container > div > a {
        color: inherit;
        text-decoration: none;
    }

    .container > div > a:hover {
        text-decoration: underline;
    }

    #flyers {
        background-image: url("@/assets/braillest-stack-of-flyers.jpg");
    }

    #sl8 {
        background-image: url("@/assets/braillest-sl8-ui.png");
    }

    #dashboard {
        background-image: url("@/assets/braillest-dashboard.jpg");
    }

    #mold-render {
        background-image: url("@/assets/braillest-flyer-render.png");
    }

    #negative-mold {
        background-image: url("@/assets/braillest-negative-mold.jpg");
    }

    #transcribe {
        background-image: url("@/assets/braillest-transcribe.png");
    } 

    #mold-interface {
        background-image: url("@/assets/braillest-mold-interface.jpg");
    }

    #mold-press {
        background-image: url("@/assets/braillest-mold-press.jpg");
    }

    #repair {
        background-image: url("@/assets/braillest-damaged.jpg");
    }

    #mold-result {
        background-image: url("@/assets/braillest-mold-result.jpg");
    }

    #format {
        background-image: url("@/assets/braillest-format.png");
    }

    #paginate {
        background-image: url("@/assets/braillest-paginate.png");
    }

    #donate {
        background-color: #f1c40f;
        border: 50px solid #e67e22;
        border-width: 50px 25px;
        border-color: #eea119 #e88f1f #f7ba22 #f0b314;
    }

    .vignette {
        box-shadow: inset 0px 0px 50px #333;
    }

    .donate-vignette {
        box-shadow: inset 0px 0px 50px #f7ba22;
    }
    
    .fill {
        background-size: cover !important;
    }

    .dark {
        color: #000;
        text-shadow: 0px 0px 2px #fff;
    }

    .clear-shadow {
        text-shadow: none;
    }

    .photo {
        margin: 20px;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-size: cover;
    }

    .divider {
        height: 1px;
        background-color: #333;
    }

    h1 {
        color: #fff;
        text-shadow: 0px 0px 2px #000;
        margin: 40px;
        min-height: 50vh;
        line-height: 50vh;
        font-size: 300px;
    }

    @media (max-width: 2040px) {
        h1 {
            font-size: 200px;
        }
    }

    @media (max-width: 1440px) {
        h1 {
            font-size: 100px;
        }
    }

    @media (max-width: 960px) {
        h1 {
            font-size: 70px;
        }
    }

    @media (max-width: 480px) {
        h1 {
            font-size: 40px;
        }
    }

    .caption {
        padding: 40px;
        background-size: 100% auto;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }

    h6 {
        color: #fff;
        text-shadow: 0px 0px 2px #000;
        font-size: 50px;
    }

    @media (max-width: 2040px) {
        h6 {
            font-size: 40px;
        }
    }

    @media (max-width: 1440px) {
        h6 {
            font-size: 40px;
        }
    }

    @media (max-width: 960px) {
        h6 {
            font-size: 30px;
        }
    }

    @media (max-width: 480px) {
        h6 {
            font-size: 25px;
        }
    }

    span {
        color: #eee;
        text-shadow: 0px 0px 4px #000;
        font-weight: bold;
    }
</style>
