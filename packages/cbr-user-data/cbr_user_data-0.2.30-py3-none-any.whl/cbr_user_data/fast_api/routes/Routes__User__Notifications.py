import time
from fastapi                                                                import HTTPException, BackgroundTasks
from starlette.requests                                                     import Request
from starlette.responses                                                    import StreamingResponse
from cbr_shared.cbr_backend.user_notifications.Model__User__Notification    import Model__User__Notification
from cbr_shared.cbr_backend.user_notifications.User__Notifications          import User__Notifications
from cbr_shared.cbr_backend.users.decorators.with_db_user                   import with_db_user
from osbot_fast_api.api.Fast_API_Routes                                     import Fast_API_Routes
from osbot_utils.helpers.generators.Generator_Manager                       import Generator_Manager
from osbot_utils.helpers.generators.Model__Generator_State                  import Model__Generator_State
from osbot_utils.utils.Json                                                 import json_to_str
from osbot_utils.utils.Misc                                                 import wait_for




class Routes__User__Notifications(Fast_API_Routes):
    tag               : str                 = 'notifications'
    generator_manager : Generator_Manager
    count             : int

    def generators__count(self):                                         # Return count of active SSE connections
        return {'active_count': len(self.generator_manager.generators) }

    def generators__stop_all(self):
        return {'closed_count': self.generator_manager.stop_all() }

    def generators__status(self):
        return {'status': self.generator_manager.status() }


    def user_notifications(self, request: Request) -> User__Notifications:
        db_user = request.state.db_user
        return User__Notifications(db_user=db_user)

    @with_db_user
    def create(self, request: Request, message: str):
        notification = Model__User__Notification(message=message)
        if self.user_notifications(request).add(notification):
            return {"status": "ok", "message": "Notification created", 'data':{"notification": notification.json()}}
        raise HTTPException(status_code=400, detail="Failed to create notification")

    @with_db_user
    def delete(self, request: Request, notification_id: str):
        if self.user_notifications(request).delete(notification_id):
            return {"status": "ok", "message": "Notification deleted"}
        raise HTTPException(status_code=404, detail="Notification not found")

    def generate_events(self, request: Request, wait_count=100, wait_time=1, get_generator=None):

        user_notifications = self.user_notifications(request)
        last_check         = time.time()
        generator          = get_generator()
        try:
            while wait_count > 0:
                if generator.state != Model__Generator_State.RUNNING:
                    print(f'>>> stopping generator: {generator}')
                    return
                if request.scope.get('state').get('is_disconnected') :
                    print(">>> disconnected detected, from request.scope.get('state')")
                    return

                event = {'count': wait_count,                                                           # Send heartbeat
                         'event':'heartbeat',
                         'data': {'timestamp': time.time()}}

                try:
                    data = json_to_str(event)
                    yield data
                except Exception as exception:
                    print(f'--- yield exception: {exception}')

                notifications     = user_notifications.new(last_notification_timestamp=last_check)      # Check for notifications
                notifications_ids = []
                if notifications:
                    for notification in notifications:
                        notifications_ids.append(notification.notification_id)
                        event = {'count' : wait_count,
                                 'event': 'notification',
                                 'data' : notification.json()}
                        yield json_to_str(event)
                    user_notifications.mark_delivered(notifications_ids)

                last_check = time.time()
                wait_for(wait_time)
                wait_count -= 1
        finally:
            print('>>> completed')
            generator.state = Model__Generator_State.COMPLETED



    @with_db_user
    def live_stream(self, request: Request, wait_count=50, wait_time=1):

        def get_generator():
            nonlocal target_id
            generator = self.generator_manager.generator(target_id)
            return generator

        gen            = self.generate_events(request, int(wait_count), float(wait_time), get_generator)
        target_id      = self.generator_manager.add(gen)

        return StreamingResponse(gen, media_type="text/event-stream")




    @with_db_user
    def all(self, request: Request):
        notifications = self.user_notifications(request).all()
        return {"notifications": [n.__dict__ for n in notifications]}

    @with_db_user
    def current(self, request: Request):
        notifications = self.user_notifications(request).current().notifications
        return {"notifications": [n.__dict__ for n in notifications]}

    def setup_routes(self):
        self.add_route_post  (self.create              )
        self.add_route_delete(self.delete              )
        self.add_route_get   (self.live_stream         )
        self.add_route_get   (self.current             )
        self.add_route_get   (self.all                 )
        self.add_route_get   (self.generators__count   )
        self.add_route_get   (self.generators__stop_all)
        self.add_route_get   (self.generators__status  )




