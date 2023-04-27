# FlickTrendz
University project named "FlickTrendz" for "Problem Workshop in Software Engineering 2023" course.

# Backend Flask App run configuration:

## Prerequisites
* Docker Desktop installed and running (https://www.docker.com/products/docker-desktop)
* Repository cloned

## Steps
* Using command line, navigate to your working directory, path should be something like this `/PATH/TO/PWSE`
* When you are in the working directory run this command `docker compose up`
* To rebuild project in the container run `docker compose build`

## Notes
* When container is created, you can manually run container in your docker desktop app

## Troubleshooting
It is possible to get "JWT timestamps not synchronized error", while tryining to login via google account.

The common solution is describe here [Solution](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Clock-Error-Check-that-your-system-clock-is-set-to-the-current-date-and-time-before-you-try-again.html?fbclid=IwAR1xKyYrBlBe-0zp7833-fxlUH447OhL5ehq4YcIQhp3dXcXCj_vLYY_bs8).

After you applied changes from this website you have to rebuild and rerun container.
