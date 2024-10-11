from rest_framework import serializers
from Istok_app import models
from users import models as users_models
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError
from django.http import JsonResponse

from users.managers import UserManager
# from django.contrib.auth import get_user_model
# User = get_user_model()
from users.models import CustomUser as User


#### Exceptions
class SurveyEditException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Проверьте наличие и правильность вводимых полей'

#### Exceptions


#### User
class UserDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'last_name', 'first_name', 'patronymic', 'birth_date', 'mailing',
                  'personal_data_processing', 'registration_by_code', 'is_active', 'is_verified']

class UserCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'last_name', 'first_name', 'patronymic', 'birth_date', 'mailing',
                  'personal_data_processing', 'registration_by_code']

    def create(self, validated_data):
        new_user = super(UserCreateSerializer, self).create(validated_data)
        new_user.set_password(validated_data.get('password', None))
        print('\nUserCreateSerializer create()\n')
        new_user.save()

        return new_user

    def update(self, instance, validated_data):
        validated_data.pop('password')
        super(UserCreateSerializer, self).update(instance, validated_data)

        return instance
#### User


#### Furniture
class TagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = models.Tags
        fields = ['id', 'name', 'highlight']


class FurnitureListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Furniture
        fields = ['id', 'category', 'name', 'tags', 'text', 'price', 'images',
                  'model_3d', 'time_created']
        depth = 1  # для полного отображения моделей M2M


class ExtraFurnitureListSerializer(serializers.ModelSerializer):
    recommendations = FurnitureListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Furniture
        fields = ['id', 'category', 'name', 'tags', 'text', 'price', 'images',
                  'model_3d', 'time_created', 'recommendations']
        depth = 1  # для полного отображения моделей M2M
#### Furniture


#### NewsList
class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.News
        fields = ['id', 'title', 'text', 'time_created', 'image']
#### NewsList


#### OrdersList
class OrderImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order_Image
        fields = ['id', 'image']
        # depth = 1  # для полного отображения моделей M2M


class OrderDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order_Document
        fields = ['id', 'file']
        # depth = 1  # для полного отображения моделей M2M


class OrdersListSerializer(serializers.ModelSerializer):
    order_document_set = OrderDocumentSerializer(many=True, read_only=True)
    order_image_set = OrderImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'number', 'create_date', 'shipment_date', 'status', 'address', 'order_image_set',
                  'order_document_set']
        depth = 1  # для полного отображения моделей M2M
#### OrdersList


#### Application
class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Application
        fields = ['id', 'time_created', 'user', 'text', 'last_name', 'first_name', 'patronymic', 'phone',
                  'contact_type', 'link', 'date_time', 'python_date_time']
        # depth = 1  # для полного отображения моделей M2M
#### Application


#### Сериализаторы Опросника
class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Option
        fields = ['id', 'text', 'user_input']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'text', 'multy_choice', 'options']
        depth = 1  # для полного отображения моделей M2M


class ExtraQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = ['id', 'text']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = ['text', 'user_answer']


class QuestionAndAnswerSerializer(serializers.ModelSerializer):
    question = ExtraQuestionSerializer(read_only=False, many=False)
    answers = AnswerSerializer(read_only=False, many=True)

    class Meta:
        model = models.QuestionAndAnswer
        fields = ['id', 'question', 'answers']
        depth = 1  # для полного отображения моделей M2M


class SurveySerializer(serializers.ModelSerializer):
    question_and_answers = QuestionAndAnswerSerializer(read_only=True, many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    dependable = serializers.BooleanField(required=True, label='Опросник надежен',
        help_text='Статус становится положительным в случае если опросник заполняли '
                  'больше минимального времени заполнения. При аналитике ненадежные будут вычеркиваться из выборки')

    class Meta:
        model = models.Survey
        fields = ['user', 'dependable', 'question_and_answers']
        # depth = 1  # для полного отображения моделей M2M

    def to_representation(self, instance):
        ret = super(SurveySerializer, self).to_representation(instance)
        question_and_answers = instance.questionandanswer_set.all()
        ret['new_questions_list'] = [int(_) for _ in instance.new_questions.split()]
        ret['question_and_answers'] = QuestionAndAnswerSerializer(question_and_answers, many=True).data
        return ret

    def create(self, validated_data):
        user = self.validated_data.pop('user')

        try:
            dependable = validated_data.pop('dependable')
            instance = models.Survey.objects.create(user=user, dependable=dependable)
            question_and_answers = self.initial_data.pop('question_and_answers')
        except Exception:
            raise Http404("Возможные ошибки:\n"
                          "Опросник данного пользователя уже существует.\n"
                          "Отсутствует поле question_and_answers.\n"
                          "Отсутствует поле dependable.")

        for obj in question_and_answers:
            answers = []
            for answer_obj in obj['answers']:
                try:
                    text = answer_obj['text']
                    if not text:
                        raise Http404

                    user_answer = answer_obj['user_answer']
                except Exception:
                    raise Http404('Проверьте наличие полей text, user_answer')

                answer_lst = models.Answer.objects.filter(text=text)
                if answer_lst.exists():
                    new_answer = answer_lst.first()
                else:
                    new_answer = models.Answer.objects.create(text=text, user_answer=user_answer)
                answers.append(new_answer)

            try:
                question_id = obj['question']['id']
            except Exception:
                raise Http404('Отсутствует ключ question, id у answers')


            new = models.QuestionAndAnswer.objects.filter(survey=instance, question=question_id)
            if new.exists():
                new = new.first()
                new.answers.set(answers)
            else:
                new = models.QuestionAndAnswer.objects.create(survey=instance, question_id=obj['question']['id'])
                new.answers.set(answers)

        return instance


    def update(self, instance, validated_data):

        try:
            dependable = validated_data.pop('dependable')
            models.Survey.objects.update(dependable=dependable)  #todo проверить вроден не должно пахать
            question_and_answers = self.initial_data.pop('question_and_answers')
        except Exception:
            raise Http404("Возможные ошибки: "
                          "Отсутствует поле question_and_answers. "
                          "Отсутствует поле dependable.")

        for obj in question_and_answers:
            answers = []
            for answer_obj in obj['answers']:

                try:
                    text = answer_obj['text']
                    if not text:
                        raise Http404

                    user_answer = answer_obj['user_answer']
                except Exception:
                    raise Http404('Проверьте наличе полей text, user_answer у answers')

                answer_lst = models.Answer.objects.filter(text=text)
                if answer_lst.exists():
                    new_answer = answer_lst.first()
                else:
                    new_answer = models.Answer.objects.create(text=text, user_answer=user_answer)
                answers.append(new_answer)

            if not answers:
                raise Http404("Проверьте наличие поля answers")
            try:
                question_id = obj['question']['id']
            except Exception:
                raise Http404('Отсутствует ключ question или id у question_and_answers')

            new = models.QuestionAndAnswer.objects.filter(survey=instance, question=question_id)
            if new.exists():
                new = new.first()
                new.answers.set(answers)
            else:
                print('instance == ', instance)
                new = models.QuestionAndAnswer.objects.create(survey=instance, question_id=question_id)
                new.answers.set(answers)
        instance.check_questions()
        return instance
#### Сериализаторы Опросника


#### Loyalty Benefit Offer(User_app)
class BenefitSerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Benefit
        fields = ['id', 'title', 'about']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Offer
        fields = ['id', 'title', 'about', 'offer_to_all']


class LoyaltySerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Loyalty
        fields = ['user_id', 'card_number', 'show_user_name', 'balance', 'balance_history', 'code', 'benefits_history',
                  'offers', 'new_benefits_count', 'benefit_to_choose']
        depth = 1

    def to_representation(self, instance):
        ret = super(LoyaltySerializer, self).to_representation(instance)
        offer_to_all = users_models.Offer.objects.filter(offer_to_all=True)
        ret['offers'] = ret['offers'] + OfferSerializer(offer_to_all, many=True).data
        ret['all_benefits'] = BenefitSerializer(users_models.Benefit.objects.all(), many=True).data

        return ret


class LoyaltyBenefitSerializer(serializers.ModelSerializer):
    # loyalty = LoyaltySerializer(read_only=True, many=False)
    # benefit = BenefitSerializer(read_only=True, many=False)

    class Meta:
        model = users_models.LoyaltyBenefit
        fields = ['id', 'benefit']
        # depth = 1
#### Loyalty Benefit Offer(User_app)


#### WebsiteSettings
class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebsiteSettings
        fields = ['name', 'min_write_time']
        depth = 1
#### WebsiteSettings



###### Куски кода для возможного использования
# user = serializers.HiddenField(default=serializers.CurrentUserDefault())
######



