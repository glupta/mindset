<template>
  <div class="home-wellnesscard-multi">
    <div class="relative-wrapper1">
      <div class="headercolor"></div>
      <p class="cardtitle">Wellness Habit #1</p>
    </div>
    <div class="flex-wrapper1">
      <div class="home-wellnesshabit-piegraph">
        <img
          alt="path"
          class="path1"
          src="https://static.overlay-tech.com/assets/0bb444fb-5d1f-4390-b586-e9e72b2379a2.svg"
        />
      </div>
      <p class="num-7-8">7 / 8</p>
    </div>
    <p class="habit">Drink water</p>
    <div class="home-wellnesshabit-number">
      <div class="relative-wrapper1">
        <div class="entrybox"></div>
        <p class="entrytext">Count</p>
      </div>
      <div class="plus">
        <img
          alt="path"
          class="path2"
          src="https://static.overlay-tech.com/assets/2e11d434-6603-48f4-93f3-d4eb0f06a28c.svg"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeWellnessCard",
};
</script>

<style scoped>
.home-wellnesscard-multi {
  background-color: rgba(255, 255, 255, 1);
  border-radius: 18px;
  padding: 0px 0px 15px;
  box-shadow: 0px 3px 6px 0px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: 1px solid rgba(151, 151, 151, 0.16);
}
.relative-wrapper1 {
  margin-bottom: 16px;
  margin-left: -1px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.headercolor {
  width: 174px;
  height: 32px;
  background-color: rgba(247, 195, 79, 1);
  position: relative;
}
.cardtitle {
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: rgba(255, 255, 255, 1);
  text-align: center;
  text-transform: uppercase;
  position: absolute;
  right: 12px;
  top: 7px;
  letter-spacing: 2px;
}
.flex-wrapper1 {
  margin-bottom: 20px;
  margin-left: -1px;
  padding: 0px 0px 0px 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.num-7-8 {
  width: 46px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
  color: rgba(38, 49, 82, 1);
  text-align: center;
  letter-spacing: 2px;
}
.habit {
  width: 114px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  margin-bottom: 7px;
  margin-left: 15px;
  letter-spacing: 1px;
}

/* wellness habit pie */
.home-wellnesshabit-piegraph {
  border-radius: 50%;
  padding: 3px 3px 3px 9px;
  display: flex;
  align-items: flex-start;
  border: 1px solid rgba(249, 174, 6, 1);
  margin-right: 32px;
}
.path1 {
  width: 36px;
  height: 42px;
}

/* wellness habit number */
.home-wellnesshabit-number {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-left: 15px;
}
.relative-wrapper1 {
  margin-right: 12px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.entrybox {
  width: 72px;
  height: 38px;
  background-color: rgba(255, 255, 255, 1);
  border-radius: 5px;
  position: relative;
  border: 1px solid rgba(37, 49, 85, 0.3);
}
.entrytext {
  width: 69px;
  font-family: "Catamaran";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(37, 49, 85, 1);
  opacity: 0.7;
  position: absolute;
  right: -5px;
  top: 8px;
  letter-spacing: 1px;
}
.plus {
  padding: 7px 7px 8px 8px;
  display: flex;
  align-items: flex-start;
  background-image: url("https://static.overlay-tech.com/assets/57fde2a0-663a-4d38-832e-01aa7e4bec0f.png");
}
.path2 {
  width: 9px;
  height: 9px;
}
</style>