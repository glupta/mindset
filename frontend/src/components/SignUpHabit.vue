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
      <p class="title">WELL-BEING HABIT</p>
      <p class="body">
        What’s something you’d
        <br>
        like to work on daily?
        <br><br>
        Enter an activity you want to do consistently. We’ll match you with someone in the same mindset.
      </p>
    </div>
    <div class="signup-gh">
      <div class="rectangle"></div>
      <div class="userentry-form-empty">
        <p class="form-label-form">Daily Habit</p>
        <input v-model="habit_input" class="entrybox-form">
      </div>
      <!--div class="flex-wrapper1">
        <div class="userentry-dropdown1">
          <div class="entrybox-dd"></div>
          <p class="entrytext-dd">Days</p>
          <p class="form-label-dd">Frequency</p>
          <div class="chevron">
            <img
              alt="path"
              class="path"
              src="https://static.overlay-tech.com/assets/802de8b9-4e36-43c7-9105-f13915886d3c.svg"
            />
          </div>
        </div>
        <div class="userentry-dropdown2">
          <div class="entrybox-dd"></div>
          <p class="entrytext-dd">Days</p>
          <p class="form-label-dd">Frequency</p>
          <div class="chevron">
            <img
              alt="path"
              class="path"
              src="https://static.overlay-tech.com/assets/802de8b9-4e36-43c7-9105-f13915886d3c.svg"
            />
          </div>
        </div>
      </div-->
    </div>
    <div class="controls-pagination-dots-light-3-dots">
      <div class="center">
        <div class="controls-pagination-dots-x-light-page-dot dot-1"></div>
        <div class="controls-pagination-dots-x-light-page-dot dot-1 dot-grey"></div>
        <div class="controls-pagination-dots-x-light-page-dot dot-grey"></div>
      </div>
    </div>
    <p class="next" @click="onSelectNext">NEXT</p>
  </div>
</template>

<script>
import router from '@/router';
export default {
  name: 'SignUpHabit',
  data () {
    return {
      habit_input: '',
      phone_num: ''
    }
  },
  mounted() {

    //check cookie to stay logged in
    if (this.$cookies.isKey('mindset')) {
      let cookie_obj = this.$cookies.get('mindset');
      if (cookie_obj.hasOwnProperty('session_hash')) {
        this.session_hash = cookie_obj.session_hash;
        fetch('/api/checkhash?h=' + this.session_hash)
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            let obj_remove = this.$cookies.remove('mindset');
            router.push({ name: "Home4" });
            return;
          }
          response.json().then(data => {
            if ('error' in data) {
              alert(data['error']);
              let obj_remove = this.$cookies.remove('mindset');
              router.push({ name: "Home4" });
            }
            else if ('habit_name' in data) {
              console.log("logged in:",data);
              if (data['habit_name']) {
                router.push({ name: "HomeSelfInfo" });
              }
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    }
    else {
      router.push({ name: "Home4" });
    }
  },
  methods: {
    onSelectNext() {
      if (this.habit_input == '') {
        alert("Oops! Something went wrong. Please enter a habit.");
      }
      else if (this.habit_input.length > 30) {
        alert("Oops! Something went wrong. Please shorten your habit.");
      }
      else {
        var entry = {
          session_hash: this.session_hash,
          habit_name: this.habit_input
        };
        fetch('/api/newhabit', {
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
            else if ('success' in data) {
              router.push({ name: "HomeSelfInfo" });
            }
            else {
              alert("Oops! Something went wrong. Please enter your habit again.")
            }
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
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

/* logo */
.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  margin-top: 24px;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}
.title {
  width: 159px;
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

/* g&h */
.signup-gh {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 0 0 15px 15px;
  padding: 0px 0px 17px;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(151, 151, 151, 0.16);
  margin-bottom: 8px;
}
.rectangle {
  width: 329px;
  height: 16px;
  background-color: rgba(247, 195, 79, 1);
  margin-bottom: 16px;
  margin-left: -1px;
}
.flex-wrapper1 {
  margin-left: -1px;
  padding: 0px 0px 0px 25px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

/* user entry form */
.userentry-form-empty {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 24px;
  margin-left: 24px;
}
.entrybox-form {
  width: 263px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 8px;
}

::placeholder {
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  letter-spacing: 1px;
}

.entrytext-form {
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
.form-label-form {
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

/* user entry dropdown */
.userentry-dropdown1 {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-right: 24px;
}
.userentry-dropdown2 {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-right: 24px;
}
.entrybox-dd {
  width: 105px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
}
.entrytext-dd {
  width: 69px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  left: 10px;
  bottom: 8px;
  letter-spacing: 1px;
}
.form-label-dd {
  width: 102px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  opacity: 0.7;
  position: absolute;
  right: 1px;
  top: 0px;
  letter-spacing: 1px;
}
.chevron {
  padding: 0px 0px 1px 1px;
  display: flex;
  align-items: flex-start;
  position: absolute;
  right: 12px;
  bottom: 15px;
}
.path {
  width: 5px;
  height: 9px;
}

/* pagination dots */
.controls-pagination-dots-light-3-dots {
  padding: 7px 81px 6px 80px;
  display: flex;
  align-items: flex-start;
  margin-bottom: 53px;
}
.center {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.dot-1 {
  margin-right: 9px;
}
.controls-pagination-dots-x-light-page-dot {
  width: 7px;
  height: 7px;
  background-color: rgba(0, 0, 0, 1);
  border-radius: 50%;
}

.dot-grey {
  background-color: rgb(169, 169, 169);
}
</style>