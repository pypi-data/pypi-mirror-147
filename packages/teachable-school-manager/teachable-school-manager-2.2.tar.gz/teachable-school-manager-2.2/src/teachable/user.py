# -*- coding: utf-8 -*-
import datetime
import time
from .school import School
# from .course import Lecture
import logging
import string
import secrets
from operator import itemgetter
from datetime import timedelta


class User:
    def __init__(self, api, email):
        self.api = api
        self._info = None
        self.email = email.strip() if api.check_email(email.strip()) else None
        #        self._email = self.email = email.strip()
        self._name = None
        #        self._name = None
        self._id = None
        self._reportcard = None
        self._exists = None
        self._notified = None
        self._school = None
        self._courses = None
        self._detailed_stats = None
        self.logger = logging.getLogger(__name__)

    @property
    def reportcard(self):
        # TODO: the reportcard gets deleted once a user is unenrolled from a course
        # However the stats get preserved in the detailed stats
        # I need to figure out if it's worth to get the summary stats from the
        # detailed stats view
        if not self._reportcard or self.api.usecache is False:
            if self.info:
                self._reportcard = self.api.get_user_report_card(self.id)
        return self._reportcard

    @property
    def name(self):
        # name getter property
        if not self._name and self.info:
            self._name = self.info.get('name').strip()
        return self._name

    @name.setter
    def name(self, name):
        # name setter property
        if not self.info:
            # we allow setting the name only if the user does not exist already
            # on the server side
            self._name = name
        else:
            self.logger.error("Can't set the name of {} as it already exists on Teachable".
                              format(self._name))

    @property
    def school(self):
        # school getter property
        if not self._school:
            self._school = School(self.api)
        return self._school

    @property
    def detailed_stats(self):
        # school getter property
        if not self._detailed_stats:
            self._detailed_stats = self.get_detailed_stats()
        return self._detailed_stats

    @property
    def notified(self):
        # notified getter property
        if not self._notified:
            self._notified = self.api.get_last_notif(self.email)
        return self._notified

    @notified.setter
    def notified(self, newdate):
        # notified setter property
        self.api.set_last_notif(self.email, newdate)
        self._notified = newdate

    #    @property
    #    def email(self):
    #        # email getter property
    #        if not self._email and self.info:
    #            self._email = self.info.get('email').strip()
    #        return self._email
    #
    #    @email.setter
    #    def email(self, email):
    #        if self.api.check_email(email):
    #            print('Setting email')
    #            self._email = email
    #        else:
    #            self._email = None
    #        print(self._email)
    #        return self._email

    @property
    def id(self):
        if not self._id:
            if self.info:
                self._id = self.info.get('id')
        return self._id

    @property
    def exists(self):
        if not self._exists:
            if self.info:
                self._exists = True
                self.email = self.info.get('email')
            else:
                self._exists = False
        return self._exists

    @property
    def info(self):
        if self.email:
            if not self._info or self.api.usecache is False:
                self._info = self.api.get_user_info(self.email)
                if not self._info:
                    pass
                    # self.logger.info('User with {} email doesn\'t exist in this school yet'.format(self.email))
            return self._info
        else:
            return None

    @property
    def courses(self):
        # courses getter property
        if (not self._courses and self.info) or self.api.usecache is False:
            self._courses = self.api.get_enrolled_courses(self.id)
        return self._courses
    
    def create(self, course=None):
        """Create the user on the server side, if the user doesn't exist and it
        has valid email """
        if self.exists is not True:
            if self.api.check_email(self.email):
                new = self.api.add_user_to_school(self, course)
                if new['message'] == 'Users imported':
                    # self.logger.info('Waiting Teachable to update backend')
                    time.sleep(1)
                    self.api.usecache = False
                    # self.logger.debug('Refreshing info for user {}'.format(self.email))
                    property().getter(self.info)
                    self.api.usecache = True
            else:
                new = {'message': '{} is not a valid email address'.format(self.email)}
        else:
            new = {'message': 'user with email {} already exists'.format(self.email)}
        return new
    
    def change_password(self, password: str = ''):
        """
        Changes the password for the user.
        
        :param password: the new password. If not specified we generate a random password
        """
        if password != "":
            password = password
        else:
            alphabet = string.ascii_letters + string.digits
            while True:
                password = ''.join(secrets.choice(alphabet) for i in range(18))
                if (any(c.islower() for c in password)
                        and any(c.isupper() for c in password)
                        and sum(c.isdigit() for c in password) >= 3):
                    break
        self.api.change_user_password(self, password)
        return password

    def get_summary_stats(self, course_id=0):
        # school is not really needed here, since every user is only part of a specific school
        """Returns a list of lists with a summary stat for the specific user"""
        stats = []
        now = datetime.datetime.today()
        for (key, course_data) in self.reportcard.items():
            if key != 'meta':
                current_course_id = course_data.get('course_id')
                if ((course_id != 0) and current_course_id == course_id) or course_id == 0:
                    course = self.school.get_course_with_id(current_course_id)
                    percentage = course_data.get('percent_complete')
                    update_time = datetime.datetime.strptime(course_data.get('updated_at'), '%Y-%m-%dT%H:%M:%SZ')
                    days_since_last = (now - update_time).days
                    updated_at = update_time.strftime('%Y-%m-%d %H:%M:%S')
                    tot_study_time = self.get_study_time()
                    today = datetime.datetime.today()
                    iso = today.isocalendar()
                    this_week = str(iso.year)+'-'+str(iso.week)
                    week_study_time = self.get_study_time(iso_week_no=this_week)
                    stats.append([self.name, self.email, course.name, updated_at,
                                  str(percentage), days_since_last, week_study_time, tot_study_time ])
        return stats

        # user_ordered_list = sorted(output, key=itemgetter('course_percentage'), reverse=True)

    # def generate_student_progress_list(self,course, output): get_course_curriculum(course_id)
    # current_lecture_title, current_section_title = get_latest_viewed_title(course, course_id) output.append({
    # 'course_id': course_id, 'course_name': course_list[course_data].get('name'), 'course_percentage': course.get(
    # 'percent_complete'), 'course_current_lecture': current_lecture_title, 'course_current_section':
    # current_section_title})

    # def get_latest_viewed_title(self, course_id):
    #     courseStats = self.getStatisticsForCourse(course_id)
    #     completedLectures = courseStats.get('completed_lecture_ids')
    #     latestLectureId = max(completedLectures)
    #     ordered_id_list = []
    #
    #     if course.get('completed_lecture_ids'):
    #         course_curriculum = curriculum.get(course_id)
    #
    #         for section in sections:
    #             for lecture in section.get('lectures'):
    #                 ordered_id_list.append(lecture.get('id'))
    #
    #         completed_lectures = course.get('completed_lecture_ids')
    #
    # # this function to order the completed_lectures looks, # but will fail if one of the lectures gets deleted (and
    # won't appear in ordered_id_list) #ordered_completed_lectures = sorted(completed_lectures,
    # key=ordered_id_list.index) ordered_completed_lectures = sorted(completed_lectures, key=lambda k: (
    # ordered_id_list.index(k) if k in ordered_id_list else -1))
    #
    #         for section in sections:
    #             lecture_id = find(section.get('lectures'), 'id', ordered_completed_lectures[-1])
    #             if lecture_id >= 0:
    #                 lecture_name = section.get('lectures')[lecture_id].get('name')
    #                 section_name = section.get('name')
    #                 return lecture_name, section_name
    #     return '', ''

    def get_detailed_stats(self):
        """Returns a list of lists with detailed stats for the specific user

        :return: a list of lessons
        """
        data = []
        stats = self.api.get_user_course_report(self.id)
        lectures_stats = stats.get('lecture_progresses')
        old_course_id = 0
        for lectureProgress in lectures_stats:
            completed_date = datetime.datetime.strptime(lectureProgress.get('completed_at'), '%Y-%m-%dT%H:%M:%SZ')
            course_id = lectureProgress.get('course_id')
            lecture_id = lectureProgress.get('lecture_id')
            if course_id != old_course_id:
                # Generally this will tend to be always the same for many iterations
                # Saving some processing time here.
                course = self.school.get_course_with_id(course_id)
            old_course_id = course_id
            lecture = course.get_lecture_with_id(lecture_id)
            str_cdate = completed_date.strftime("%Y-%m-%d %H:%M:%S")
            data.append([self.name, self.email, str_cdate, course.name,
                         lecture.name, lecture.duration_as_text])
        return data

    def get_last_lecture(self):
        """Returns a list containing the information of the last lecture completed,
        with data on when it was completed

        :return: list
        """
        data = []
        stats = self.api.get_user_course_report(self.id)
        progress = stats.get('lecture_progresses')
        if progress:
            last_lecture = progress[0]
            completed_date = datetime.datetime.strptime(last_lecture.get('completed_at'), '%Y-%m-%dT%H:%M:%SZ')
            course_id = last_lecture.get('course_id')
            lecture_id = last_lecture.get('lecture_id')
            course = self.school.get_course_with_id(course_id)
            lecture = course.get_lecture_with_id(lecture_id)
            str_cdate = completed_date.strftime("%Y-%m-%d %H:%M:%S")
            data = [self.name, str_cdate, course.name,
                    lecture.name, lecture.duration_as_text]
        return data

    def get_study_time(self, tolerance=60, iso_week_no=None, start_day=None, end_day=None):
        """Returns an estimate of the amount of time the student has been studying

        :param tolerance: the tolerance in minutes to apply to consecutive lessons to count them
                          as one single session. Default: 60 minutes. If two lessons are taken
                          within a distance lower than tolerance they are counted as consecutive.
        :param iso_week_no: restrict the calculation to the ISO week number
               in the format YYYY-WW, e.g. 2021-41
        :param start_day: restrict the calculation to after this day in the format YYYY-MM-DD
        :param end_day: restrict the calculation to before this day in the format YYYY-MM-DD


        :return: a datetime.timedelta object with the amount of study time
        """
        stats = self.detailed_stats
        # We define an arbitrary tolerance of one hour here
        # assuming if the user has interrupted the study for more than one hour
        # then it means s/he's done something else in the meantime
        tolerance = timedelta(minutes=tolerance)
        tot = timedelta(0)
        problems = False
        if start_day:
            try:
                start_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
            except Exception as e:
                self.logger.error('Malformed date: {}'.format(start_day))
                self.logger.error(e)
                problems = True
        if end_day:
            try:
                end_day = datetime.datetime.strptime(end_day, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
            except Exception as e:
                self.logger.error('Malformed date: {}'.format(end_day))
                self.logger.error(e)
                problems = True
        if iso_week_no and (start_day or end_day):
            self.logger.error('Please use either iso_week_no or start_day and/or end_day')
            problems = True
        elif iso_week_no:
            try:
                year, week = iso_week_no.split('-')
                start_day = datetime.datetime.fromisocalendar(int(year), int(week), 1)
                end_day = datetime.datetime.fromisocalendar(int(year), int(week), 7) + \
                          timedelta(hours=23, minutes=59, seconds=59)
            except Exception as e:
                self.logger.error("Can't understand ISO week number {}".format(iso_week_no))
                self.logger.error(e)
                problems = True

        if stats and not problems:
            stats.sort(key=lambda x: datetime.datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))
            for i in range(0, len(stats) - 1):
                start_good = True
                end_good = True
                t1 = datetime.datetime.strptime(stats[i][2], '%Y-%m-%d %H:%M:%S')
                t2 = datetime.datetime.strptime(stats[i + 1][2], '%Y-%m-%d %H:%M:%S')
                if start_day:
                    if t1 <= start_day or t2 <= start_day:
                        start_good = False
                if end_day:
                    if t1 >= end_day or t2 >= end_day:
                        end_good = False
                diff = t2 - t1
                if diff <= tolerance and start_good and end_good:
                    tot += diff
        return tot

    def is_enrolled_to_course(self, course_id):
        """Returns true if user is enrolled to courseId"""
        return self.api.check_enrollment_to_course(self.id, course_id)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)

    def __repr__(self):
        return '<User({})>'.format(self.email)

    def enroll(self, course):
        return self.api.enroll_user_to_course(self, course)

    def unenroll(self, course):
        return self.api.unenroll_user_from_course(self, course)
