<template>
  <div class="iphone-11-pro-max-copy-12">
    <div class="logo">
      <div class="path-2">
        <div class="mask">
          <img
            alt="shape"
            class="shape"
            src="https://static.overlay-tech.com/assets/f2d389ed-c7ca-4222-83b5-907922cdfe87.png"
          />
        </div>
        <img
          alt="inside-shadow"
          class="inside-shadow"
          src="https://static.overlay-tech.com/assets/ca8ab436-e678-4b89-b488-0b118dc96fd7.svg"
        />
      </div>
      <img
        alt="mindset"
        class="mindset"
        src="https://static.overlay-tech.com/assets/20797dca-1c84-441a-a948-55e77bc68eff.svg"
      />
    </div>
    <div class="signup-titletext">
      <p class="title">WELCOME BACK</p>
      <p v-if="login_bool" class="body">
        A socially accountable way
        <br>
        to build well-being habits
      </p>
      <p v-if="!login_bool" class="body">
        Thank you for your interest in the Mindset community!
        <br><br>
        We texted you a link, click to login.
      </p>
    </div>
    <div v-if="login_bool" class="signup-signin">
      <div class="flex-wrapper1">
        <p class="num-431">&#43;1</p>
        <div class="relative-wrapper1">
          <p class="form-label">Mobile Number</p>
          <input class="entrybox" @keypress="isNumber($event)" v-model="mobile_input">
        </div>
      </div>
      <!--div class="userentry-form-empty">
        <p class="form-label-pw">Password</p>
        <input type="password" class="entrybox-pw" v-model="pw_input">
      </div>
      <p class="action-forgotpass">FORGOT PASSWORD</p-->
      <p class="form-label-copy">
        New to MINDSET?
        <strong class="formlabelcopyemphasis2" @click="onSelectSignUp">Sign Up</strong>
      </p>
      <!--div class="flex-wrapper2">
        <p class="terms-amp-conditions">TERMS &amp; CONDITIONS</p>
        <p class="privacy-policy">PRIVACY POLICY</p>
      </div-->
    </div>
    <!--p v-if="!login_bool" class="signup-submit">
      Thank you for your interest in the Mindset community!
      <br><br>
      We texted you a link. Please click to login.
    </p-->
    <p v-if="login_bool" class="next" @click="onSelectNext">NEXT</p>
  </div>
</template>

<script>
import router from '@/router';
export default {
  name: 'Home4',
  data () {
    return {
      mobile_input: "",
      pw_input: "",
      login_bool: true
    }
  },
  mounted() {

    //verified from sign up
    if (this.$route.query.i) {
      fetch('/api/verifyphone?i=' + this.$route.query.i)
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
            let cookie_obj = new Object();
            cookie_obj.session_hash = this.$route.query.i;
            let cookie_json = JSON.stringify(cookie_obj);
            this.$cookies.set('mindset',cookie_json,-1);
            console.log("create cookie");
            router.push({ name: "SignUpHabit" });
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }

    //verified from login
    else if (this.$route.query.l) {
      fetch('/api/verifylogin?l=' + this.$route.query.l)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {
          if ('error' in data) {
            alert(data['error']);
          }
          else if ('habit_name' in data) {
            let cookie_obj = new Object();
            cookie_obj.session_hash = this.$route.query.l;
            let cookie_json = JSON.stringify(cookie_obj);
            this.$cookies.set('mindset',cookie_json,-1);
            console.log("create cookie");

            if (data['habit_name']) {
              router.push({ name: "HomeSelfInfo" });
            }
            else {
              router.push({ name: "SignUpHabit" });
            }
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }

    //check cookie to auto login
    if (this.$cookies.isKey('mindset')) {
      let cookie_obj = this.$cookies.get('mindset');
      if (cookie_obj.hasOwnProperty('session_hash')) {
        this.session_hash = cookie_obj.session_hash;
        fetch('/api/checkhash?h=' + this.session_hash)
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
          }
          response.json().then(data => {
            if ('error' in data) {
              alert(data['error']);
              let obj_remove = this.$cookies.remove('mindset');
              console.log("delete:",obj_remove);
            }
            else if ('habit_name' in data) {
              if (data['habit_name']) {
                router.push({ name: "HomeSelfInfo" });
              }
              else {
                router.push({ name: "SignUpHabit" });
              }
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    }
  },
  methods: {
    onSelectNext() {
      let mobile_clean = this.mobile_input.replace(/\D/g,'');
      console.log("before:",this.mobile_input,"after:",mobile_clean);
      if (mobile_clean.length != 10) {
        alert("Oops! Something went wrong. Please enter your 10-digit mobile number.");
        return;
      }
      /*
      if (this.pw_input == "") {
        alert("Oops! Something went wrong. Please enter your password.");
        return;
      }
      */
      var entry = {
        phone_num: mobile_clean,
        //password: this.pw_input,
      };
      fetch('/api/login', {
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
            this.login_bool = false;
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },
    onSelectSignUp() {
      router.push({ name: "SignUp" });
    },
    isNumber: function(evt) {
      evt = (evt) ? evt : window.event;
      var charCode = (evt.which) ? evt.which : evt.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
        evt.preventDefault();;
      } else {
        return true;
      }
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
  width: 100%;
  height: 100%;
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

::placeholder {
  width: 214px;
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
}

/*logo css*/
.logo {
  margin-top: 24px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
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

/* title & text */
.signup-titletext {
  width:;
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  width: 160px;
  font-family: "Catamaran";
  font-size: 18px;
  font-weight: 700;
  line-height: normal;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  margin-bottom: 4px;
  letter-spacing: 2px;
}
.body {
  max-width: 280px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  text-align: center;
  opacity: 0.7;
  letter-spacing: 1px;
}

/* signin */
.signup-signin {
  padding: 22px 82px 0px 82px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 16px;
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
  width: 20px;
}
.relative-wrapper1 {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.entrybox {
  width: 225px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}
.entrytext {
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
  left: -38px;
  top: -22px;
  letter-spacing: 1px;
}
.action-forgotpass {
  width: 280px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  text-decoration: underline;
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.form-label-copy {
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
.formlabelcopyemphasis2 {
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
  padding: 0px 0px 0px 17px;
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

/*user entry form */
.userentry-form-empty {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 10px;
}
.entrybox-pw {
  width: 280px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}
.entrytext-pw {
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
.form-label-pw {
  /*width: 261px;*/
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  position: absolute;
  /*right: 0px;*/
  left: 0px;
  top: 0px;
  letter-spacing: 1px;
}
</style>