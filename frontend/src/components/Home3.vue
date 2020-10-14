<template>
  <div class="mobile-test01">
    <!--div class="group"><div class="num-01"></div></div-->
    <div class="path-2">
      <div class="mask">
        <img
          alt="shape"
          class="shape"
          src="@/assets/img/Logo_182x310.svg"
        />
      </div>
      <img
        alt="inside-shadow"
        class="inside-shadow"
        src="https://static.overlay-tech.com/assets/b19d6902-a934-4e15-adc7-cd73a2a61792.svg"
      />
    </div>
    <img
      alt="mindset"
      class="mindset"
      src="@/assets/img/MINDSET@3x.svg"
    />
    <p class="please-leave-your-na">
      WE ARE A SELECTIVE COMMUNITY OF HIGH ACHIEVERS, PASSIONATE ABOUT WELLBEING AND PERSONAL GROWTH.
    </p>
    <p class="sign-up">{{header_text}}</p>
    <div v-if="submit_bool" class="relative-wrapper1">
      <div class="num-02"></div>
      <div class="num-03"></div>
      <p class="name">Full Name</p>
      <input v-model="name_input" placeholder="Liz Smith" class="name-box">
      <!--p class="password">Password</p>
      <div class="rectangle-copy"></div>
      <p class="">***********</p>
      <p class="confirm-password">Confirm Password</p>
      <div class="rectangle-copy-2"></div>
      <p class="-copy">***********</p-->
      <p class="phone-number-copy-2">Mobile Number</p>
      <p class="num-431-copy-2">&#43;1</p>
      <input v-model="phone_input" placeholder="2345678901" class="phone-box">
      <div class="group-3" @click="onSubmitNext">
        <p class="next">SUBMIT</p>
      </div>
    </div>
    <div v-if="!submit_bool" class="relative-wrapper1">
      <div class="num-02"></div>
      <div class="num-03"></div>
      <p class="submit-text">
        {{submit_text1}}
        <br><br>
        {{submit_text2}}
      </p>
    </div>
  </div>
</template>

<script>
import router from '@/router';
export default {
  name: "Home3",
  data () {
    return {
      submit_bool: true,
      name_input: "",
      phone_input: "",
      header_text: "Join our waiting list",
      submit_text1: "",
      submit_text2: ""
    }
  },
  mounted() {
    if (this.$route.query.i) {
      this.submit_bool = false;
      this.header_text = "Verifying...";
      fetch('/api/verifyphone?i=' + this.$route.query.i)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {
          if ('error' in data) {
            alert(data['error']);
            this.header_text = "Join our waiting list";
            this.submit_bool = true;
          }
          else {
            console.log("phone:",data);
            this.submit_bool = false;
            this.header_text = "You're all set!";
            this.submit_text1 = "You have been added to our waiting list.";
            this.submit_text2 = "Our team will be in touch in the coming days. :)"
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  },
  methods: {
    onSubmitNext() {

      if (this.name_input == "") {
        alert("Oops! Something went wrong. Please enter your name.");
        return;
      }

      if (this.phone_input == "") {
        alert("Oops! Something went wrong. Please enter your phone number.");
        return;
      }

      if (this.name_input.length > 40) {
        alert("Oops! Something went wrong. Please shorten your name.");
        return;
      }

      let phone_input_clean = this.phone_input.replace(/\D/g,'');
      if (phone_input_clean.length != 10) {
        alert("Oops! Something went wrong. Please enter a 10-digit phone number.");
        return;
      }

      console.log("phone:",phone_input_clean);

      //capture phone number
      fetch('/api/phoneintake?p=' + phone_input_clean + '&n=' + this.name_input)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {
          if ('error' in data) {
            alert(data['error']);
          }
          else {
            console.log("phone:",data);
            this.submit_bool = false;
            this.header_text = "Verify your number";
            this.submit_text1 = "Thank you for your interest in the Mindset community!";
            this.submit_text2 = "We texted you a link. Please click to verify your mobile number.";
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  },
  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'MINDSET' || 'Some Default Title';
      }
    }
  }
};
</script>

<style scoped>

.mobile-test01 {
  padding: 0px 0px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.group {
  margin-bottom: 40px;
  padding: 44px 120px 4px;
  display: flex;
  align-items: flex-start;
  background-image: url("https://static.overlay-tech.com/assets/61a5a437-2028-4ebb-aa35-fc3afc77b13d.png");
}
.num-01 {
  width: 172px;
  height: 20px;
  background-color: rgba(246, 247, 248, 1);
}
.path-2 {
  margin-top: 24px;
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.mask {
  padding: 0px 0px 1px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.shape {
  width: 74px;
  height: 126px;
}
.inside-shadow {
  width: 50px;
  height: 116px;
  position: absolute;
  left: 17px;
  top: -3px;
}
.mindset {
  width: 129px;
  height: 20px;
  margin-bottom: 32px;
}
.sign-up {
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  margin-bottom: 4px;
  letter-spacing: 2px;
}
.please-leave-your-na {
  max-width: 291px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  margin-bottom: 24px;
  opacity: 0.7;
  letter-spacing: 1px;
}
.relative-wrapper1 {
  /*margin-bottom: 64px;*/
  display: flex;
  align-items: flex-start;
  position: relative;
}
.num-02 {
  width: 336px;
  height: 272px;
  /*width: 100%;
  height: 351px;*/
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 0 0 15px 15px;
  box-shadow: 0px 3px 5px 0px rgba(110, 122, 169, 0.2);
  position: relative;
}
.num-03 {
  width: 336px;
  /*width: 100%;*/
  height: 16px;
  background-color: rgba(37, 49, 85, 1);
  position: absolute;
  left: 0px;
  top: 0px;
}
.name-box {
  width: 246px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: absolute;
  left: 35px;
  top: 54px;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}

::placeholder {
  width: 214px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
}
.rectangle-copy {
  width: 246px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  /*position: absolute;
  left: 35px;*/
  top: 132px;
  border: 1px solid rgba(37, 49, 85, 0.3);
}
.rectangle-copy-2 {
  width: 246px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  /*position: absolute;
  left: 35px;*/
  bottom: 100px;
  border: 1px solid rgba(37, 49, 85, 0.3);
}
.phone-box {
  width: 212px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: absolute;
  /*right: 50px;*/
  /*bottom: 24px;*/
  top: 132px;
  left: 69px;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}
.name-text {
  width: 214px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  position: absolute;
  left: 42px;
  top: 64px;
  letter-spacing: 2px;
}
/*
. {
  width: 203px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  position: absolute;
  left: 42px;
  top: 144px;
  letter-spacing: 2px;
}
*/
.-copy {
  width: 203px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  position: absolute;
  left: 42px;
  bottom: 113px;
  letter-spacing: 2px;
}
.num-000-000-0000-copy-2 {
  width: 203px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  position: absolute;
  right: 50px;
  bottom: 33px;
  letter-spacing: 2px;
}
.num-431-copy-2 {
  width: 26px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  position: absolute;
  left: 35px;
  /*bottom: 33px;*/
  top: 141px;
  letter-spacing: 2px;
}
.name {
  width: 193px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 35px;
  top: 32px;
  letter-spacing: 2px;
}
.password {
  width: 193px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 35px;
  top: 110px;
  letter-spacing: 2px;
}
.confirm-password {
  width: 193px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 35px;
  bottom: 145px;
  letter-spacing: 2px;
}
.phone-number-copy-2 {
  width: 193px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 35px;
  /*bottom: 67px;*/
  top: 110px;
  letter-spacing: 2px;
}
.group-3 {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 28px;
  padding: 17px 35px;
  box-shadow: 2px 4px 6px 0px rgba(113, 113, 113, 0.21);
  /*display: flex;
  align-items: flex-start;*/
  position: absolute;
  top: 196px;
  left: 94px;
  border: 1px solid rgba(54, 69, 135, 0.25);
  cursor: pointer;
}
.next {
  width: 76px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  color: rgba(54, 69, 135, 1);
  text-align: center;
  letter-spacing: 2px;
}

.submit-text {
  width: 266px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 35px;
  top: 35px;
  letter-spacing: 2px;
}
</style>