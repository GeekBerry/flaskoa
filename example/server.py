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
    @Router.post('')
    @middleware
    def create(self, body, **_):
        self.logger.info('create teacher', body)
        return body

    @Router.get('/<teacher_id>')
    def query(self, teacher_id: str, **_):
        return 'teacher' + teacher_id


class Professor(Teachers):
    @Router.get('/<teacher_id>/papers')
    def query_papers(self, teacher_id, query, **_):
        page_size = int(query.get('pagesize', 10))

        return [f'paper {i} author {teacher_id}' for i in range(page_size)]


class School(App):
    @App.post('/login')
    def login(self, query, **_):
        self.logger.info('login: ', query)
        return 'login'


if __name__ == '__main__':
    app = School()

    app.use('/', health)

    app.use('/v1', Router()
        .use('/teachers', Teachers())
        .use('/professors', Professor())
        )

    app.run(host='127.0.0.1', port=5000, debug=True)
