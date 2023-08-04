<template>
  <v-row justify="center">
    <v-dialog
        v-model="showDialog"
        persistent
        max-width="500px"
    >

      <v-card class="d-flex align-center justify-center" style="font-family: Arial, sans-serif;">
        <v-card-title class="d-flex align-center justify-center">
          {{ passwordText }}
        </v-card-title>
        <div style="display: flex; flex-direction: row">
          <v-otp-input
              class="mb-4"
              ref="otpInput"
              v-model:value="bindModal"
              input-classes="otp-input"
              separator="-"
              :num-inputs="4"
              :should-auto-focus="true"
              input-type="letter-numeric"
              :conditionalClass="['one', 'two', 'three', 'four']"
              :placeholder="['*', '*', '*', '*']"
          />
        </div>

        <v-btn style="font-family: Arial, sans-serif;"
               variant="tonal"
               color=#FBC02D
               @click="clearInput()">
          Clear password
        </v-btn>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn style="font-family: Arial, sans-serif;"
                 variant="tonal"
                 color="#00C853"
                 @click="checkPassword()"
          >
            Enter
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup lang="ts">
import {ref} from "vue";
import VOtpInput from "vue3-otp-input";
import {v4 as uuidv4} from 'uuid';

var passwordText = ref('Insert the password');

let showDialog = ref(true);

const otpInput = ref<InstanceType<typeof VOtpInput> | null>(null);
const bindModal = ref();

const clearInput = () => {
  otpInput.value?.clearInput();
};

function checkPassword(this: any) {
  if (bindModal.value == import.meta.env.VITE_FRONTEND_PW) {
    showDialog.value = false;
    const uuid: string = uuidv4();
    sessionStorage.setItem("id", uuid);
  } else {
    passwordText.value = "Wrong password, try again";
  }
}


</script>


<style>
.otp-input {
  width: 40px;
  height: 40px;
  padding: 5px;
  margin: 0 10px;
  font-size: 20px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.3);
  text-align: center;
}

/* Background colour of an input field with value */
.otp-input.is-complete {
  background-color: #e4e4e4;
}

.otp-input::-webkit-inner-spin-button,
.otp-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input::placeholder {
  font-size: 15px;
  text-align: center;
  font-weight: 600;
}
</style>