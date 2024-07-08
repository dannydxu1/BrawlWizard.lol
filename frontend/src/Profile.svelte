<script>
  import { onMount } from "svelte";
  import { location } from "svelte-spa-router";

  let profileID = "";
  let profileData = {};
  let loading = true;
  let error = null;

  function geBrawlerNameForImages(name) {
    if (name.toUpperCase() === "R-T") return "R-T";

    if (name.toUpperCase() === "MR. P") return "Mr._P";

    if (name.toUpperCase() === "LARRY & LAWRIE") return "Larry_%26_Lawrie";

    // Default case: capitalize the first letter, lowercase the rest
    return name
      .toLowerCase()
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join("_");
  }

  // Fetch data when the component mounts
  onMount(async () => {
    profileID = $location.split("/").pop(); // Get the last part of the URL
    console.log("Profile ID:", profileID);

    if (!profileID) {
      console.error("Profile ID is undefined.");
      return;
    }

    try {
      console.log(
        `Fetching data from http://127.0.0.1:5000/api/player/${profileID}`
      );
      const response = await fetch(
        `http://127.0.0.1:5000/api/player/${profileID}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch profile data");
      }
      profileData = await response.json();
      console.log("Profile Data:", profileData);
    } catch (err) {
      error = err.message;
      console.error("Error fetching profile data:", error);
    } finally {
      loading = false;
      console.log("Loading state set to false");
    }
  });
</script>

<div class="profile-container">
  {#if loading}
    <div class="loading">Fetching profile data, please wait...</div>
  {:else if error}
    <div class="error">Error: {error}</div>
  {:else}
    <div class="profile-details">
      <h2>Profile: {profileData.name}</h2>
      <p>Tag: {profileData.tag}</p>
      <p>Trophies: {profileData.trophies}</p>
      <p>Highest Trophies: {profileData.highestTrophies}</p>
      <p>3v3 Victories: {profileData["3vs3Victories"]}</p>
      <p>Solo Victories: {profileData.soloVictories}</p>
      <p>Duo Victories: {profileData.duoVictories}</p>
      <div class="club-details">
        <h3>Club</h3>
        <p>Name: {profileData.club.name}</p>
        <p>Tag: {profileData.club.tag}</p>
      </div>
      <div class="top-brawlers">
        <h3>Top Brawlers</h3>
        {#each profileData.topBrawlers as brawler}
          <div class="brawler-card">
            <img
              src={`images/Brawler_Portrait/${geBrawlerNameForImages(brawler.name)}_Portrait.png`}
              alt={brawler.name}
              class="brawler-image"
            />
            <p>Name: {geBrawlerNameForImages(brawler.name)}</p>
            <p>Highest Trophies: {brawler.highestTrophies}</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .profile-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .loading,
  .error {
    font-size: 1.5em;
    text-align: center;
    margin-top: 20px;
  }

  .profile-details {
    background-color: #1a237e;
    color: #e8eaf6;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }

  .club-details,
  .top-brawlers {
    margin-top: 20px;
  }

  .brawler-card {
    background-color: #283593;
    border-radius: 10px;
    padding: 20px;
    margin-top: 10px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }

  .brawler-card p {
    color: #fff;
  }

  .brawler-image {
    width: 100px;
    height: 100px;
    object-fit: cover;
    object-position: top;
    border-radius: 5px;
    margin-bottom: 10px;
  }
</style>
