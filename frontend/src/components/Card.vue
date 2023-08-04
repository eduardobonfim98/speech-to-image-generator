<template>
  <div class="main-container">
    <div class="text-center">
      <v-dialog
          v-model="alertEmptyPrompt"
          activator="parent"
          width="auto"
      >
        <v-card>
          <v-card-text
              style="color: #000000; font-size: 18px; font-weight: 500;">
            Please enter a prompt
          </v-card-text>
          <v-card-actions>
            <v-btn color="orange" block @click="closeAlert ">Close Dialog</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </div>
    <div class="text-center">
      <v-dialog
          v-model="alertMaxCharacters"
          activator="parent"
          width="auto"
      >
        <v-card>
          <v-card-text
              style="color: #000000; font-family: Arial, sans-serif; font-size: 18px; font-weight: 500;">
            The maximum number of characters is 600.
          </v-card-text>
          <v-card-actions>
            <v-btn color="orange" block @click="closeAlert "
                   style="color: #000000; font-family: Arial, sans-serif; font-size: 18px; font-weight: 500;">
              Close Dialog
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div class="image-container">
      <img class="top-left-image" :src="logo" :class="{ 'responsive-image': true, 'mobile-size-image': true }">
    </div>
    <div flat class="mt-10">
      <v-container class="d-flex justify-center"
                   style="color: #0d47a1; font-family: Arial, sans-serif; font-size: 18px; font-weight: 550; text-align: center;">
        <h1>Speech-Text to Image Generator</h1>
      </v-container>
      <v-container class="d-flex justify-center align-center"
                   style="color: #0d47a1; font-family: Arial, sans-serif; font-size: 18px; font-weight: 550;">
        <div class="d-flex flex-column justify-center align-center" style="text-align: center;">
          <p>1-) Choose the language you want to transcript your prompt or write it directly in English</p>
          <p>2-) Enhance your prompt for better results</p>
          <p>3-) Generate your image</p>
        </div>
      </v-container>
    </div>

    <loading v-model:active="isLoading"
             :can-cancel="false"
             loader="dots"
             color="#0064a6"
             :is-full-page="fullPage"/>

    <v-container class="d-flex justify-center">
      <div class="custom-font">
        <v-select class="mr-4 justify-space-around"
                  style="max-width: 80px; max-lenght: 50px; height: 40px; font-size: 16px; background-color: #FFFFFF; border-radius: 20px;font-family: Arial, sans-serif;"
                  density="compact"
                  variant="solo"
                  v-model="audioLanguage"
                  :items="['DE', 'CH']"
        ></v-select>
      </div>
      <v-btn v-if="isRecordingSupported" @click="toggleRecording"
             :class="['recording-button', { 'recording': recording }]">
        {{ recording ? 'Stop Recording' : 'Start Recording' }}
      </v-btn>
      <v-btn v-else :class="['disabled-button']">
        Not Supported
      </v-btn>
    </v-container>
    <div>
      <v-container fluid
                   style="color: #000000; font-family: Arial, sans-serif; font-size: 18px; font-weight: 500;">
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6">
            <div style="position: relative;">
              <v-textarea
                  style="font-family: Arial, sans-serif; color: #000000;"
                  counter
                  :rules="rules"
                  v-model="prompt"
                  align-center rows="3"
                  no-resize
                  label='Describe what you want to see
                  (E.g. "Mountains on Mars")'
                  variant="solo">
              </v-textarea>
              <v-btn @click="clearText" icon small class="v-textarea__icon"
                     style="position: absolute; right: 8px; top: 10px; width: 24px; height: 24px; color: #000000;">
                <v-icon style="font-size: 16px;">$close</v-icon>
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
      <div class="d-flex flex-row justify-center" style="margin-bottom: 16px;">
        <v-btn class="mr-4" @click="enhancePrompt"
               style="height: 40px; border-radius: 9px; text-align: center; color: #000000; font-size: 13px; font-weight: 250;">
          Enhance prompt
        </v-btn>
        <v-btn @click="loadComponent"
               :style="{
         height: '40px',
         borderRadius: '9px',
         textAlign: 'center',
         color: '#000000',
         fontSize: '13px',
         fontWeight: '250',
       }"
               :disabled=generating>
          {{ generating ? 'Generating Images' : 'Generate Images' }}
        </v-btn>
      </div>
    </div>
  </div>

  <div style="background-color:#F2F4EB">
    <v-container v-if="isComponentLoaded"
                 class="mx-auto d-flex align-center justify-center" flat
                 style="max-width: 1000px; background-color: #F2F4EB">
    </v-container>
    <div ref="scrollToDiv">
      <v-card v-if="isComponentLoaded" :key="placeholderCounter"
              class="mx-auto d-flex align-center justify-center" flat
              style="background-color: #F2F4EB; max-width: 1000px; max-height: 1000px;
                    margin-bottom: 15px;">
        <v-row>
          <v-col
              v-for="(imageData, n) in images"
              :key="n"
              class="d-flex child-flex"
              cols="6"
          >
            <v-img
                :src="imageData"
                :lazy-src="screen"
                aspect-ratio="1"
                cover
            >
              <template v-slot:placeholder>
                <v-row
                    class="fill-height ma-0"
                    align="center"
                    justify="center"
                >
                  <v-progress-circular
                      :size="70"
                      :width="7"
                      color="purple"
                      indeterminate
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-col>
        </v-row>
      </v-card>
    </div>

    <v-dialog
        v-model="dialog"
        fullscreen
        :scrim="false"
        transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ props }">
        <div class="custom-button-container">
          <v-btn
              class="custom-large-btn"
              color="#0d47a1"
              icon="mdi-light mdi-comment-question-outline"
              v-bind="props"
              x-large
          ></v-btn>
        </div>
      </template>
      <v-card
          style="background-color: #F2F4EB; ">
        <v-toolbar
            dark
            color="#0d47a1"
        >
          <v-btn
              icon
              dark
              @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title style="color:  #F2F4EB; font-family: Arial, sans-serif;">How does it work?</v-toolbar-title>
        </v-toolbar>
        <v-carousel
            hide-delimiters
            show-arrows="hover"
            style="background-color: #F2F4EB; width: 100%; height: 100%; padding: 30px"
        >
          <v-carousel-item
              v-for="(item, i) in items"
              :key="i"
              :src="item.src"
              fill-height
          ></v-carousel-item>
        </v-carousel>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';
import {MediaRecorder} from 'extendable-media-recorder';
import {AudioApiFactory} from "@/apis/audio-api";
import {Gpt3ApiFactory} from "@/apis/gpt3-api";
import {StableDiffusionApiFactory} from "@/apis/stable-diffusion-api";
import {Configuration} from "@/configuration";

const config = new Configuration({"username": "foo", "password": import.meta.env.VITE_FRONTEND_PW});

const gpt3_factory = Gpt3ApiFactory(config);
const audio_factory = AudioApiFactory(config);
const stableDiffusion_factory = new StableDiffusionApiFactory(config);
import logo from '../assets/logo.png';
import screen from '../assets/screen.png';
import slide1 from '../assets/slide1.png';
import slide2 from '../assets/slide2.png';
import slide3 from '../assets/slide3.png';
import slide4 from '../assets/slide4.png';
import slide5 from '../assets/slide5.png';
import slide6 from '../assets/slide6.png';

export default {
  data() {

    return {
      logo: logo,
      screen: screen,
      recording: false,
      generating: false,
      slide1: slide1,
      slide2: slide2,
      slide3: slide3,
      slide4: slide4,
      slide5: slide5,
      slide6: slide6,
      mediaRecorder: null,
      isRecordingSupported: false,
      chunks: [],
      audioURL: null,
      isComponentLoaded: false,
      isLoading: false,
      fullPage: true,
      prompt: '',
      placeholderCounter: 0,
      alertEmptyPrompt: false,
      alertMaxCharacters: false,
      dialog: false,
      notifications: false,
      sound: true,
      widgets: false,
      items: [
        {
          src: slide1,
        },
        {
          src: slide2,
        },
        {
          src: slide3,
        },
        {
          src: slide4,
        },
        {
          src: slide5,
        },
        {
          src: slide6,
        },
      ],
      audioId: null,
      isAudioLoaded: false,
      audioTranslated: null,
      audioLanguage: 'CH',

      promptEnhancedId: null,
      enhancedPrompt: null,

      imagesArrayId: null,
      areImagesArrayLoaded: false,
      imagesArray: null,
      imageData0: '',
      imageData1: '',
      images: [
        this.imageData0,
        this.imageData1,
      ],
    }
  },
  components: {
    Loading
  },
  methods: {
    enhancePrompt() {
      if (this.prompt !== '' && (this.prompt.length < 600)) {
        let p = {"prompt": this.prompt, "sessionId": sessionStorage.getItem("id"), "actionId": "1"};
        console.log("Sending gpt-3 request to the backend")
        this.gpt3Post(p);
        this.isLoading = true;

      } else if (this.prompt == '') {
        this.alertEmptyPrompt = true;

      } else if (this.prompt.length > 600) {
        this.alertMaxCharacters = true;
      }
    },
    loadComponent() {
      if (this.prompt !== '' && (this.prompt.length < 600)) {
        this.isComponentLoaded = true;
        console.log("Sending generate image request to the backend")
        let p = {
          "promptEnhanced": this.enhancedPrompt,
          "numberOfImages": 4,
          "numberOfInferenceSteps": 50,
          "height": 512,
          "width": 512,
          "sessionId": sessionStorage.getItem("id"),
          "actionId": "2"
        };
        if (this.placeholderCounter !== 0) {
          this.imageData0 = logo;
          this.imageData1 = logo;
        }
        this.stableDiffusionPost(p);
        this.generating = true;
        this.placeholderCounter += 1;
        this.$nextTick(() => {

          const scrollToDiv = this.$refs.scrollToDiv

          scrollToDiv.scrollIntoView({behavior: "smooth"});
        });

      } else if (this.prompt == '') {
        this.alertEmptyPrompt = true;

      } else if (this.prompt.length > 600) {
        this.alertMaxCharacters = true;
      }

    },
    checkMediaDevicesSupport() {
      const isDesktopBrowser = !/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      if (isDesktopBrowser && 'mediaDevices' in navigator) {
        console.log("getUserMedia supported.");
        this.isRecordingSupported = true;
      } else {
        console.log("getUserMedia not supported on mobile.");
        this.isRecordingSupported = false;
      }
    },
    toggleRecording() {
      if (this.recording) {
        this.stopRecording();
      } else {
        this.startRecording();
      }
    },
    startRecording() {
      if (navigator.mediaDevices) {
        console.log("getUserMedia supported.");
        navigator.mediaDevices.getUserMedia({audio: {sampleRate: 16000}})
            .then(stream => {
              this.mediaRecorder = new MediaRecorder(stream, {mimeType: 'audio/webm'});
              this.mediaRecorder.addEventListener("dataavailable", event => {
                this.chunks.push(event.data);
                const reader = new FileReader();
                reader.readAsDataURL(event.data);
                const that = this;
                reader.onloadend = function () {
                  const base64data = reader.result;
                  console.log("Sending audio request to the backend")
                  let p = {
                    "blobData": base64data,
                    "sessionId": sessionStorage.getItem("id"),
                    "actionId": "3",
                    "audioLanguage": that.audioLanguage
                  }
                  that.audioPost(p)
                }
              });
              this.mediaRecorder.addEventListener("stop", () => {
                this.recording = false;
              });
              this.mediaRecorder.start();
              this.recording = true;
            })
            .catch(error => {
              console.error(error);
            });
      }
    },
    stopRecording() {
      this.isLoading = true;
      this.mediaRecorder.stop();
    },

    //*************** gpt3 ***************//

    gpt3Post(data) {
      gpt3_factory.gpt3Post(data)
          .then(response => {
            this.startPollingGpt3(response.data.promptEnhancedId);
            return response;
          })
          .catch(error => {
            console.log(error);
          });
    },

    startPollingGpt3(promptEnhancedId) {
      let intervalId = setInterval(async () => {
        const result = await this.promptEnhancedPolling(promptEnhancedId);
        this.enhancedPrompt = result.data.promptEnhancedContent;
        if (result.data.promptEnhancedContent !== "None") {
          this.isLoading = false;
          this.prompt = result.data.promptEnhancedContent;
          clearInterval(intervalId);
        }
      }, 1000);
    },

    promptEnhancedPolling(promptEnhancedId) {
      return gpt3_factory.gpt3PromptEnhancedIdGet(promptEnhancedId)
          .then(response => {
            return response;
          })
          .catch(error => {
            console.log(error);
          });
    },

    //*************** Audio ***************//

    audioPost(data) {
      audio_factory.audioPost(data)
          .then(response => {
            this.startPollingAudio(response.data.audioId)
          })
          .catch(error => {
            console.log(error);
          });
    },

    startPollingAudio(audioId) {
      let intervalId = setInterval(async () => {
        const result = await this.audioGetPolling(audioId);
        if (result.data.audioContent !== undefined) {
          this.prompt = result.data.audioContent;
          this.isLoading = false;
          clearInterval(intervalId);
        }
      }, 10000);

    },

    audioGetPolling(audioId) {
      return audio_factory.audioAudioIdGet(audioId)
          .then(response => {
            return response;
          })
          .catch(error => {
            console.log(error);
          });
    },
    //*************** stableDiffusion ***************

    stableDiffusionPost(data) {
      stableDiffusion_factory.stableDiffusionGenerateImagesPost(data)
          .then(response => {
            this.startPollingStableDiffusion(response.data.imagesArrayId)
            return response;
          })
          .catch(error => {
            console.log(error);
          });
    },

    startPollingStableDiffusion(stableDiffusionId) {
      let intervalId = setInterval(async () => {
        const result = await this.stableDiffusionPolling(stableDiffusionId);
        if ((result.data.imageArrayContent).length !== 0) {
          const images = result.data.imageArrayContent.map((image) => {
            const img = new Image();
            img.src = `data:image/jpeg;base64,${image.imageContent}`;
            return img.src;
          });
          this.images = images;
          this.isLoading = false;
          if ((result.data.images_progress) === 'done') {
            this.generating = false
            clearInterval(intervalId);
          }
        }
      }, 2000);
    }
    ,

    stableDiffusionPolling(stableDiffusionId) {
      return stableDiffusion_factory.stableDiffusionGenerateImagesImagesArrayIdGet(stableDiffusionId)
          .then(response => {
            return response;
          })
          .catch(error => {
            console.log(error);
          });
    }
    ,
    clearText() {
      this.prompt = "";
    }
    ,
    closeAlert() {
      this.alertEmptyPrompt = false;
      this.alertMaxCharacters = false;
    }
    ,
  },
  watch: {
    prompt(newVal) {
      this.enhancedPrompt = newVal;
    }
  },
  computed: {
    rules() {
      return [(v) => v.length <= 600 || 'Max 600 characters'];
    },
  },
  mounted() {
    this.checkMediaDevicesSupport();
  },
};

</script>

<style>

.main-container {
  position: relative;
  background-color: #F2F4EB;
  height: 130%;
}

.top-left-image {

  position: absolute;
  top: 20px;
  left: 20px;
  width: 5%;
}

.custom-font {
  font-family: Arial, sans-serif;
}

.responsive-image {
  width: 100%;
  height: auto;
  display: block;
}

.image-container {
  position: relative;
}

.mobile-size-image {
  max-width: 30px;
  max-height: 30px;
}

.custom-button-container {
  margin-bottom: 40px;
  margin-left: 40px;
}

.custom-large-btn {
  height: 400px;
  width: 400px;
  font-size: 400px;
}

/* Media query for mobile devices */
@media (min-width: 700px) {
  .mobile-size-image {
    max-width: 400px;
    max-height: 400px;
    width: 80px;
    height: 80px;
  }
}

/* Define styles for larger screens (default) */
.multiline-label .v-label {
  white-space: normal;
}

/* Media query for smaller screens (e.g., mobile devices) */
@media screen and (max-width: 350px) {
  .multiline-label .v-label {
    white-space: nowrap;
    margin-bottom: 100px;
  }
}

.recording-button {
  height: 40px;
  border-radius: 9px;
  text-align: center;
  color: #000000;
  font-size: 13px;
  font-weight: 250;
  cursor: pointer;
}

.recording-button.recording {
  background-color: rgb(255, 41, 41);
}

.disabled-button {
  height: 40px;
  border-radius: 9px;
  text-align: center;
  color: #ffffff;
  font-size: 13px;
  font-weight: 250;
  background-color: gray;
}


</style>


