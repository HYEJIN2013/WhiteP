// users_controller.js    index() {
      User.query()        .where({tweets__body__icontains: 'Minecraft'}) // add me        .join('tweets', {body__icontains: 'Minecraft'}) // add me        .end((err, models) => {          this.respond(err || models, ['tweets']); // add me        });
    }
