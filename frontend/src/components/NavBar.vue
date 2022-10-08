<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
		<div class="container-fluid">
			<router-link class="navbar-brand" to="/">NSS</router-link>
			<!-- <a class="navbar-brand" href="#">NSS</a> -->
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
			  <span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarSupportedContent">
			  <ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
					  Refuelings
					</a>
					<ul class="dropdown-menu" aria-labelledby="navbarDropdown">
						<li> <router-link class="dropdown-item" :to="{name: 'AddRefuel'}">Add</router-link></li>
						<li><hr class="dropdown-divider"></li>
						<li><router-link class="dropdown-item" :to="{name: 'List'}">List</router-link></li>
					</ul>
				</li>
				<router-link class="nav-link active" :to="{name: 'Diary'}">Diary</router-link>
			  </ul>
			  <!-- <form class="d-flex">
				<input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
				<button class="btn btn-outline-success" type="submit">Search</button>
			  </form> -->
			  <ul class="navbar-nav" v-if="isAuthenticated()">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false"> {{isAuthenticated()}} </a>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
						<li><router-link class="dropdown-item" :to="{name: 'Settings'}">Settings</router-link></li>
                        <li><router-link class="dropdown-item" :to="{name: 'Login'}">Logout</router-link></li>
                    </ul>
				</li>
			  </ul>
			  
			</div>
		</div>
	</nav>
</template>

<script>
import {mapGetters} from "vuex"
export default {
    name: "NavBar",
	methods:{
		...mapGetters("auth", [
			"isAuthenticated"
		])
	}
}
</script>