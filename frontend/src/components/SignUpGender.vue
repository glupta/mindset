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
      <p class="title">YOUR INFO</p>
      <p class="body">
        Tell your partner
        <br>
        about yourself
        <br><br>
        What is your gender?
      </p>
    </div>
    <div class="userentry-form-empty">
      <p class="form-label3">Gender</p>
      <select class="form-control" @change="changeAge($event)">
        <option value="" selected disabled>Choose</option>
        <option v-for="input in gender_inputs" :value="input.id" :key="input.id">{{ input.name }}</option>
      </select>
    </div>
    <p class="next" @click="onSelectNext">NEXT</p>
  </div>
</template>

<script>
import router from '@/router';
export default {
  name: 'SignUpGender',
  data () {
    return {
      gender_input: '',
      phone_num: '',
      session_hash: '',
      gender_inputs: [
      { name: "Female", id: 1 },
      { name: "Male", id: 2 },
      { name: "Non-binary", id: 3 } ],
      selected_input: null
    }
  },
  mounted() {

    //this.age_input = this.age_input_options[0];

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
            else if ('phone_num' in data) {
              this.phone_num = data['phone_num'];
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
      if (this.selected_input == null) {
        alert("Oops! Something went wrong. Please select a gender.");
      }
      else {
        console.log("selected:",this.selected_input);
        //call server to store gender in DB
        let fetch_url = '/api/genderupdate?h=' + this.session_hash + '&g=' + this.selected_input;
        fetch(fetch_url) //get weekly habit count
        .then(response => {
          if (response.status !== 200) { //server error handling
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
          }
          response.json().then(data => {
            if ('error' in data) { //error handling from testroom backend call
              console.log("gender error: ",data['error']);
              alert("gender error: " + data['error']);
              return;
            }
            else if ('success' in data) {
              console.log("gender added!");
              router.push({ name: "SignUpBio" });
            }
            return data;
          });
        })
        .catch(error => { //error handling
          console.log("Fetch error: " + error);
        });
      }
    },
    changeAge(event) {
      this.selected_input = event.target.options[event.target.options.selectedIndex].text
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

.path {
  width: 14px;
  height: 8px;
}

.userentry-form-empty {
  padding: 22px 0px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
  margin-bottom: 24px;
  margin-left: 24px;
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

.entrybox {
  width: 263px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.age-text {
  margin-left: 20px;
}

.userentry-dropdown1 {
  margin-right: 20px;
}

/* drop down */
.userentry-form-dropdown {
  display: flex;
  flex-direction: column;
  align-items: center;

  width: 263px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}
.form-label-dd {
  width: 261px;
  font-family: "Catamaran";
  font-size: 14px;
  font-weight: 200;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-transform: uppercase;
  margin-left: 4px;
  opacity: 0.7;
  letter-spacing: 1px;
}
.relative-wrapper1-dd {
  display: flex;
  align-items: center;
  align-items: center;
  position: relative;
  flex-direction: column;
  justify-content: space-around;
}
.entrybox-dd {
  width: 273px;
  height: 198px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  border: 1px solid rgba(37, 49, 85, 0.3);

  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}
.entrytext-dd {
  /*width: 240px;*/
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  /*
  position: absolute;
  left: 10px;
  top: 8px;*/
  letter-spacing: 1px;
}
.option1 {
  width: 240px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  /*
  position: absolute;
  left: 10px;
  top: 48px;
  */
  letter-spacing: 1px;
}
.option2 {
  width: 240px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  /*
  position: absolute;
  left: 10px;
  top: 88px;
  */
  letter-spacing: 1px;
}
.option3 {
  width: 240px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  /*
  position: absolute;
  left: 10px;
  bottom: 48px;
  */
  letter-spacing: 1px;
}
.option4 {
  width: 240px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  /*
  position: absolute;
  left: 10px;
  bottom: 8px;
  */
  letter-spacing: 1px;
}
.dividers {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  left: 10px;
  top: 39px;
}
.divider1 {
  width: 238px;
  background-color: rgba(216, 216, 216, 1);
  border-radius: 1px;
  opacity: 0.15;
  border: 1px solid rgba(151, 151, 151, 1);
/*  &:not(:last-of-type) {
    margin-bottom: 38px;
  }*/
}

.form-control {
  width: 273px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
  padding-left: 10px;
}
</style>