from flaskoa import App, Router


def middleware(func):
    def _(*args, **kwargs):
        print('BEFORE', args, kwargs)
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            print('EXCEPT', e)
            raise
        else:
            print('SUCCESS', ret)
            return ret
        finally:
            print('AFTER')

    return _


@Router.get('')
def health(app, **_):
    app.logger.debug('health')
    return True


class Teachers(Router):
    @Router.post('/')
    @middleware
    def create(self, body, **_):
        self.logger.info('create teacher', body)
        return body

    @Router.get('/<teacher_id>')
    def query(self, teacher_id: str, **_):
        return 'teacher' + teacher_id


class Students(Router):
    @Router.post('/')
    def create(self, body, **_):
        self.logger.info('create student', body)
        return body

    @Router.get('/<student_id>')
    def query(self, student_id: str, **_):
        return 'student' + student_id


class School(App):
    @App.post('/login')
    def login(self, query, **_):
        self.logger.info('login: ', query)
        return 'login'


if __name__ == '__main__':
    app = School()

    v1 = Router() \
        .use('/teachers', Teachers()) \
        .use('/students', Students())

    app.use('/', health).use('/v1', v1)

    app.run(host='127.0.0.1', port=5000, debug=True)
