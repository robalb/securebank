<script>
  export let currentPage;
  import logo from '../assets/chart1-4.png'
  import '../assets/bootstrap.css'
  import '../assets/win95.css'
  import Footer from './Footer.svelte'
  let navOpen = false;

  function togglenav(){
    navOpen = !navOpen;
  }

  let pages=[
    {
      slug: "/", name: "Main Panel"
    },
    {
      slug: "/transfer/", name: "Transfer"
    },
  ]
</script>

<nav class="navbar navbar-expand-lg navbar-light navbar-95 ">
        <a class="navbar-brand" href="/">
            <img src={logo} alt="Logo" width="32" height="32" > SecureBank</a>
        <button on:click={togglenav} 
          class="navbar-toggler " type="button" aria-controls="navbar-dropdown"
          aria-expanded={navOpen} aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse {navOpen && 'show'}" id="navbar-dropdown" >
            <ul class="navbar-nav" style="align-items: end; padding: .5rem" >
              {#each pages as page}
                <li class="nav-item {page.slug==currentPage && 'active'}">
                    <a class="nav-link" href={page.slug}>{page.name}
                    {#if page.slug==currentPage}
                      <span class="sr-only">(current)</span>
                    {/if}
                    </a>
                </li>
              {/each}
                <li class="nav-item">
                    <a class="nav-link" href="http://localhost:8080/docs">
                      APIdocs
                    </a>
                </li>
            </ul>
        </div>
</nav>
<main>
<slot />
</main>
<Footer/>
