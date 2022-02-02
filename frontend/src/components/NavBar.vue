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
						<li> <router-link class="dropdown-item" to="/add-refuel">Add</router-link></li>
						<li><hr class="dropdown-divider"></li>
						<li><a class="dropdown-item" href="#">List</a></li>
					</ul>
				</li>
				<router-link class="nav-link active" to="/diary">Diary</router-link>
			  </ul>
			  <form class="d-flex">
				<input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
				<button class="btn btn-outline-success" type="submit">Search</button>
			  </form>
			</div>
		</div>
	</nav>
</template>

<script>
export default {
    name: "NavBar",
}
</script>