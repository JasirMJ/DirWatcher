import os
from django.shortcuts import render

# Create your views here.
from dirwatcher.GlobalFunctions import *
from dirwatcher.GlobalImports import *
from dirwatcher.DynamicFieldsModel import DynamicFieldsModelSerializer


from django.shortcuts import render

from dirRecord.models import DirFiles, DirectoryRecords

# Begin : Serializers For This Project
class DirFilesSerializer(DynamicFieldsModelSerializer):
    class Meta : 
        model = DirFiles
        fields = '__all__'
        exclude_list = []

class DirectoryRecordSerializer(DynamicFieldsModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta : 
        model = DirectoryRecords
        fields = [ "id", "name", "path", "created_at", "updated_at", "is_deleted", "files",]
        exclude_list = []

    def get_files(self,obj):
        files = DirFiles.objects.filter(record=obj)
        serializer = DirFilesSerializer(files,many=True)
        return serializer.data

# End : Serializers For This Project


# Begin : API End Point Logic

class DirRecordAPI(ListAPIView):
    serializer_class = DirectoryRecordSerializer

    def get(self,request):
        path = self.request.GET.get("path", "all")
        if path == "":
            return ResponseFunction(0, "Path is required", {})
        listDir = []
        try:
            if path != "all" : listDir = os.listdir(path)
        except Exception as e:
            return ResponseFunction(0, str(e), {})
        obj = dirMonitorChecker(path,listDir)
        return ResponseFunction(1, "", DirectoryRecordSerializer(obj).data)

    # def get_queryset(self):
    #     return DirectoryRecords.objects.all()

    def post(self, request):
        required = ["name","path"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'],{})
        else:
            print("Receved required Fields")

        try:
            id = self.request.POST.get("id", "")
            obj = create_or_update_dir_record(request.data,id)

            return ResponseFunction(1, obj.msg, DirectoryRecordSerializer(obj.obj).data)
        except Exception as e:
            printLineNo()
            print("Excepction ", printLineNo(), " : ", e)
            return ResponseFunction(0,f"Excepction occured {str(e)}",{})

    def delete(self, request):
        try:
            id = self.request.GET.get('id', "[]")
            if id == "all":
                DirectoryRecords.objects.all().delete()
                return ResponseFunction(1, "Deleted all data",{})
            else:
                id = json.loads(id)
                DirectoryRecords.objects.filter(id__in=id).delete()
                return ResponseFunction(1, "Deleted data having id " + str(id),{})

        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

class DirFilesAPI(ListAPIView):
    serializer_class = DirFilesSerializer

    def get_queryset(self):
        return DirFiles.objects.all()

    def post(self, request):
        required = ["name","record"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'],{})
        else:
            print("Receved required Fields")

        try:
            id = self.request.POST.get("id", "")
            obj = create_or_update_dir_files(request.data,id)
            return ResponseFunction(1, obj['msg'], DirFilesSerializer(obj['obj']).data)
        except Exception as e:
            print("Excepction : ", printLineNo(), " : ", e)
            return ResponseFunction(0,f"Excepction occured {str(e)}",{})

def create_or_update_dir_record(data,id):
    '''General function for create or update record'''
    msg = ""
    if id:
        print("Country Updating")
        qs = DirectoryRecords.objects.filter(id=id)
        if not qs.count():
            return ResponseFunction(0, "Country Not Found", {})
        obj = qs.first()
        serializer = DirectoryRecordSerializer(obj, data=data, partial=True)
        msg = "Data updated"
    else:
        print("Adding new Country")
        serializer = DirectoryRecordSerializer(data=data, partial=True)
        msg = "Data saved"
    serializer.is_valid(raise_exception=True)

    obj = serializer.save()
    return {"obj":obj,"message":msg}
    
def create_or_update_dir_files(data,id):
    '''General function for create or update files'''
    msg = ""
    if id:
        print("Country Updating")
        qs = DirFiles.objects.filter(id=id)
        if not qs.count():
            return ResponseFunction(0, "Country Not Found", {})
        obj = qs.first()
        serializer = DirFilesSerializer(obj, data=data, partial=True)
        msg = "Data updated"
    else:
        print("Adding new Country")
        serializer = DirFilesSerializer(data=data, partial=True)
        msg = "Data saved"
    serializer.is_valid(raise_exception=True)

    obj = serializer.save()
    return {"obj":obj,"message":msg}

def dirMonitorChecker(path,listDir):
    '''
    if the value of path is 'all' then it will check all the recorded paths from DirectoryRecords table
    else it will monitor specified path
    '''

    if path=="all":
        for record in DirectoryRecords.objects.all():
            listDir = os.listdir(record.path)
            print("lst Dir ",listDir)
            dirMonitor(record.path,listDir)
    else:
        return dirMonitor(path,listDir)

def dirMonitor(path,listDir):

    qs = DirectoryRecords.objects.filter(name=path)
    if not qs:
        data = {
            "name":path,
            "path":path,
        }
        obj = create_or_update_dir_record(data,"")
        obj = obj['obj']
    else:
        obj = qs[0]

    files_obj = DirFiles.objects.filter(record=obj)

    with transaction.atomic():
        files_obj.update(is_deleted=True,deleted_at=datetime.datetime.now())
        obj_files_array = []
        for paths in listDir:
            if files_obj.filter(name=paths).exists():
                files_obj.filter(name=paths).update(is_deleted=False,deleted_at=None)
            else:
                dataFile = { "name":paths, }
                serializer = DirFilesSerializer(data=dataFile)
                serializer.is_valid(raise_exception=True)
                obj_file = serializer.save(record=obj)
                obj_files_array.append(obj_file.id)

        print("obj_files_array ",obj_files_array)
    return obj

# End : API End Point Logic