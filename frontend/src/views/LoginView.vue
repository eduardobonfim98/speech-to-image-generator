
<script>
import axios from "axios";
import Card from '../components/Card.vue'
import Dialog from '../components/Dialog.vue'
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';
export default {
  components: {
    Card, Dialog, Loading
  },
  data() {
    return {
      message: '',
    };
  },
  methods: {
    sendMessage() {
      axios.post('https://160.85.252.37:8000/', {
        message: this.message,
      })
      .then(response => {
        console.log("Message sent");
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
    },
  },
};

</script>

<template>
  <Card/>
  <Dialog/>
</template>

<style>

</style>

