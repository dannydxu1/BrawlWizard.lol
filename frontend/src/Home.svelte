<script>
  import { link } from "svelte-spa-router";

  let message = "Welcome to the Home Page!";
  let profileID = "";

  function getProfile() {
    if (profileID.trim() !== "") {
      window.location.href = `/#/profile/${profileID}`; // Use link to navigate to the profile page
    }
  }
</script>

<div class="home-container">
  <h1>{message}</h1>
  <p>This is the home page of your Svelte application.</p>
  <p>Feel free to explore and modify this page to suit your needs.</p>
  <div class="input-container">
    <input type="text" bind:value={profileID} placeholder="Enter Profile ID" />
    <button on:click={getProfile}>Get Started</button>
  </div>
</div>

<style>
  body {
    background-color: #1a237e;
    color: #e8eaf6;
    font-family: "Arial", sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .home-container {
    background-color: #283593;
    border-radius: 10px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  }

  h1 {
    color: #ffeb3b;
    font-size: 3em;
    margin-bottom: 20px;
  }

  p {
    font-size: 1.2em;
    margin-bottom: 20px;
  }

  .input-container {
    margin-top: 20px;
  }

  input[type="text"] {
    padding: 10px;
    font-size: 1em;
    border: none;
    border-radius: 5px;
    margin-right: 10px;
    width: calc(100% - 120px);
    box-sizing: border-box;
  }

  button {
    padding: 10px 20px;
    font-size: 1em;
    color: #283593;
    background-color: #ffeb3b;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #fdd835;
  }
</style>
