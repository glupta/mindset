<template>
  <div class="iphone-11-pro-max-copy-12">
    <div class="logo">
      <div class="path-2">
        <div class="mask">
          <img
            alt="shape"
            class="shape"
            src="https://static.overlay-tech.com/assets/8ce84555-8b83-4202-962b-74bc460e4cbe.png"
          />
        </div>
        <img
          alt="inside-shadow"
          class="inside-shadow"
          src="https://static.overlay-tech.com/assets/25377353-e0bd-4ed2-b10d-62ccbee0d74f.svg"
        />
      </div>
      <img
        alt="mindset"
        class="mindset"
        src="https://static.overlay-tech.com/assets/6b271a4c-4599-48eb-8d13-a3197ddbba67.svg"
      />
    </div>
    <div class="signup-titletext">
      <p class="title">SIGN UP</p>
      <!--p class="title">WELCOME</p-->
      <p v-if="signup_bool" class="body">
        A socially accountable way
        <br>
        to build well-being habits
      </p>
      <p v-if="!signup_bool" class="body">
        Thank you for your interest in the Mindset community!
        <br><br>
        We texted you a link. Please click to verify your mobile number.
        <br><br>
        Tip: Add our number as a contact so you can easily find us.
      </p>
    </div>
    <div v-if="signup_bool" class="signup-signup">
      <div class="userentry-form userentry-form-empty">
        <p class="form-label3">Nickname</p>
        <input class="entrybox" v-model="name_input">
      </div>
      <!--div class="userentry-form userentry-form-empty">
        <p class="form-label3">Password</p>
        <input type="password" class="entrybox" v-model="pw_input">
      </div>
      <div class="userentry-form-copy-2 userentry-form-empty">
        <p class="form-label3">Confirm Password</p>
        <input type="password" class="entrybox" v-model="confirm_input">
      </div-->
      <div class="flex-wrapper1">
        <p class="num-431">&#43;1</p>
        <div class="relative-wrapper1">
          <p class="form-label">Mobile Number</p>
          <input class="rectangle2" v-model="mobile_input">
          <!--p class="why">WHY</p-->
        </div>
      </div>
      <p class="form-label2">
        Already have an account?
        <strong class="formlabelemphasis2" @click="onSelectSignIn">Sign In</strong>
      </p>
      <!--div class="flex-wrapper2">
        <p class="terms-amp-conditions">TERMS &amp; CONDITIONS</p>
        <p class="privacy-policy">PRIVACY POLICY</p>
      </div-->
    </div>
    <!--p v-if="!signup_bool" class="signup-submit">
      Thank you for your interest in the Mindset community!
      <br><br>
      We texted you a link. Please click to verify your mobile number.
    </p-->
    <p v-if="signup_bool" class="next" @click="onSelectNext">NEXT</p>
  </div>
</template>

<script>
import router from '@/router';
export default {
  name: 'SignUp',
  data () {
    return {
      name_input: "",
      pw_input: "",
      confirm_input: "",
      mobile_input: "",
      signup_bool: true
    }
  },
  methods: {
    onSelectSignIn() {
      router.push({ name: "Home4" });
    },
    onSelectNext() {

      if (this.name_input.length < 2) {
        alert("Oops! Something went wrong. Please enter a longer name.");
        return;
      }

      if (this.name_input.length > 10) {
        alert("Oops! Something went wrong. Please shorten your name.");
        return;
      }

      let mobile_clean = this.mobile_input.replace(/\D/g,'');
      if (mobile_clean.length != 10) {
        alert("Oops! Something went wrong. Please enter a 10-digit mobile number.");
        return;
      }

      /*
      if (this.pw_input != this.confirm_input) {
        alert("Oops! Something went wrong. Your passwords do not match.");
        return;
      }

      //To check a password between 6 to 20 characters which contain at least one numeric digit, one uppercase and one lowercase letter
      const re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
      if (!re.test(this.pw_input)) {
        alert("Oops! Something went wrong. Your password should be between 6 and 20 characters, with at least one numeric digit, one uppercase and one lowercase letter.");
        return;
      }
      */

      var entry = {
        phone_num: mobile_clean,
        full_name: this.name_input,
        //password: this.pw_input,
      };
      fetch('/api/signup', {
        method: "POST",
        body: JSON.stringify(entry),
        headers: new Headers({
        "content-type": "application/json"
        })
      })
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
            console.log("sms response:",data['response']);
            this.signup_bool = false;
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  }
};
</script>

<style scoped>
.iphone-11-pro-max-copy-12 {
  padding: 0px 0px 38px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.group {
  margin-bottom: 24px;
  padding: 44px 121px 4px;
  display: flex;
  align-items: flex-start;
  background-image: url("https://static.overlay-tech.com/assets/f004dd77-93a8-4626-8b2f-c6fbefcedc93.png");
}
.rectangle {
  width: 172px;
  height: 20px;
  background-color: rgba(246, 247, 248, 1);
}
.next {
  width: 100px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  text-decoration: underline;
  letter-spacing: 2px;
  cursor: pointer;
}
.signup-submit {
  margin-bottom: 40px;
}

/*logo*/
.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 24px;
  margin-bottom: 24px;
}
.path-2 {
  margin-bottom: 11px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.mask {
  padding: 0px 1px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.shape {
  width: 59px;
  height: 101px;
}
.inside-shadow {
  width: 40px;
  height: 93px;
  position: absolute;
  left: 14px;
  top: -2px;
}
.mindset {
  width: 103px;
  height: 16px;
}

/*title & text */
.signup-titletext {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 36px;
}
.title {
  width: 159px;
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  margin-bottom: 24px;
  letter-spacing: 2px;
}
.body {
  max-width: 291px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  opacity: 0.7;
  letter-spacing: 1px;
}

/*sign up*/
.signup-signup {
  padding: 0px 82px 30px 82px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  /*margin-bottom: 12px;*/
}
.userentry-form {
  margin-bottom: 32px;
}
.userentry-form-copy-2 {
  margin-bottom: 38px;
}
.flex-wrapper1 {
  margin-bottom: 16px;
  padding: 0px 0px 0px 4px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.num-431 {
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  margin-right: 14px;
  opacity: 0.7;
  letter-spacing: 1px;
}
.relative-wrapper1 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.rectangle2 {
  width: 244px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}
.drink-water {
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 8px;
  top: 8px;
  letter-spacing: 1px;
}
.form-label {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  position: absolute;
  left: -30px;
  top: -22px;
  letter-spacing: 1px;
}
.why {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: right;
  position: absolute;
  right: 0px;
  top: -22px;
  letter-spacing: 2px;
}
.form-label2 {
  width: 280px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 300;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  margin-bottom: 24px;
  letter-spacing: 2px;
}
.formlabelemphasis2 {
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  letter-spacing: 2px;
  cursor: pointer;
}
.button-linkedin-signin {
  margin-bottom: 12px;
}
.flex-wrapper2 {
  padding: 0px 0px 0px 14px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.terms-amp-conditions {
  font-family: "Catamaran";
  font-size: 9px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  letter-spacing: 1px;
  margin-right: 46px;
}
.privacy-policy {
  font-family: "Catamaran";
  font-size: 9px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  letter-spacing: 1px;
}

/*user entry*/
.userentry-form-empty {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.entrybox {
  width: 263px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}
.entrytext {
  width: 255px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  right: 0px;
  bottom: 8px;
  letter-spacing: 1px;
}
.form-label3 {
  width: 261px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  position: absolute;
  right: 0px;
  top: 0px;
  letter-spacing: 1px;
}

::placeholder {
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
}
</style>