import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from java.util.logging import Level
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices

from database import Database
from utils import Utils
from psy.psyutils import PsyUtils

class ModulePsy:
    def __init__(self, app_name, case, log):
        self.log = log
        self.case = case
        self.context = None
        self.module_name = app_name + ": "
        self.utils = PsyUtils()
    
    def process_report(self, datasource_name, file, report_number, path):
        # Check if the user pressed cancel while we were busy
        if self.context.isJobCancelled():
            return IngestModule.ProcessResult.OK

        data = Utils.read_json(path)

        self.log(Level.INFO, " Processing messages")

        self.process_messages(data.get("messages"), file)
        self.process_user_profile(data.get("profile"), file)
        self.process_users(data.get("users"), file)
        self.process_searches(data.get("searches"), file)
        self.process_undark(data.get("freespace"), file)
        self.process_videos(data.get("videos"), report_number, file, os.path.dirname(path), datasource_name)
        self.process_logs(data.get("log"), file)

    def initialize(self, context):
        self.context = context
        # Messages attributes
        # self.att_msg_uid = self.utils.create_attribute_type('TIKTOK_MSG_UID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Uid", self.case)
        # self.att_msg_uniqueid = self.utils.create_attribute_type('TIKTOK_MSG_UNIQUE_ID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Unique ID", self.case)
        # self.att_msg_nickname = self.utils.create_attribute_type('TIKTOK_MSG_NICKNAME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Nickname", self.case)
        self.att_msg_created_time = self.utils.create_attribute_type('TIKTOK_MSG_CREATED_TIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Created TIme", self.case)
        self.att_msg_participant_1 = self.utils.create_attribute_type('TIKTOK_MSG_PARTICIPANT_1', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Participant 1", self.case)
        self.att_msg_participant_2 = self.utils.create_attribute_type('TIKTOK_MSG_PARTICIPANT_2', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Participant 2", self.case)
        self.att_msg_message = self.utils.create_attribute_type('TIKTOK_MSG_MESSAGE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Message", self.case)
        self.att_msg_read_status = self.utils.create_attribute_type('TIKTOK_MSG_READ_STATUS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Read Status", self.case)
        self.att_msg_local_info = self.utils.create_attribute_type('TIKTOK_MSG_LOCAL_INFO', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Local Info", self.case)
        self.att_msg_sender = self.utils.create_attribute_type('TIKTOK_MSG_SENDER', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Sender", self.case)
        self.att_msg_type = self.utils.create_attribute_type('TIKTOK_MSG_TYPE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Type", self.case)
        self.att_msg_deleted = self.utils.create_attribute_type('TIKTOK_MSG_DELETED', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Deleted", self.case)
        
        #profile
        self.att_prf_avatar = self.utils.create_attribute_type('TIKTOK_PROFILE_AVATAR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Avatar", self.case)
        self.att_prf_account_region = self.utils.create_attribute_type('TIKTOK_PROFILE_REGION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Region", self.case)
        self.att_prf_follower_count = self.utils.create_attribute_type('TIKTOK_PROFILE_FOLLOWER', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Followers", self.case)
        self.att_prf_following_count = self.utils.create_attribute_type('TIKTOK_PROFILE_FOLLOWING', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Following", self.case)
        self.att_prf_gender = self.utils.create_attribute_type('TIKTOK_PROFILE_GENDER', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Gender", self.case)
        self.att_prf_google_account = self.utils.create_attribute_type('TIKTOK_PROFILE_GOOGLE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Google Account", self.case)
        # self.att_prf_is_blocked = self.utils.create_attribute_type('TIKTOK_PROFILE_IS_BLOCKED', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.BYTE, "Is Blocked", self.case)
        # self.att_prf_is_minor = self.utils.create_attribute_type('TIKTOK_PROFILE_IS_MINOR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.BYTE, "Is Minor", self.case)
        self.att_prf_nickname = self.utils.create_attribute_type('TIKTOK_PROFILE_NICKNAME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Nickname", self.case)
        self.att_prf_register_time = self.utils.create_attribute_type('TIKTOK_PROFILE_REGISTER_TIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Register Time", self.case)
        self.att_prf_sec_uid = self.utils.create_attribute_type('TIKTOK_PROFILE_SEC_UID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Sec. UID", self.case)
        self.att_prf_short_id = self.utils.create_attribute_type('TIKTOK_PROFILE_SHORT_ID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Short ID", self.case)
        self.att_prf_uid = self.utils.create_attribute_type('TIKTOK_PROFILE_UID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "UID", self.case)
        self.att_prf_unique_id = self.utils.create_attribute_type('TIKTOK_PROFILE_UNIQUE_ID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Unique ID", self.case)
        self.att_prf_follow_status = self.utils.create_attribute_type('TIKTOK_PROFILE_FOLLOW_STATUS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Follow Status", self.case)
        self.att_prf_url = self.utils.create_attribute_type('TIKTOK_PROFILE_URL', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Url", self.case)

        #seaches
        self.att_searches = self.utils.create_attribute_type('TIKTOK_SEARCH', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Search", self.case)

        #undark
        self.att_undark_key = self.utils.create_attribute_type('TIKTOK_UNDARK_KEY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Database", self.case)
        self.att_undark_output = self.utils.create_attribute_type('TIKTOK_UNDARK_OUTPUT', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Output", self.case)

        #videos

        self.att_vid_key = self.utils.create_attribute_type('TIKTOK_VIDEO_KEY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Key", self.case)
        self.att_vid_last_modified = self.utils.create_attribute_type('TIKTOK_VIDEO_LAST_MODIFIED', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Last Modified", self.case)

        #logs

        self.att_log_time = self.utils.create_attribute_type('TIKTOK_LOGS_TIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Time", self.case)
        self.att_log_session = self.utils.create_attribute_type('TIKTOK_LOGS_SESSION_ID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Session ID", self.case)
        self.att_log_action = self.utils.create_attribute_type('TIKTOK_LOGS_ACTION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Action", self.case)
        self.att_log_body = self.utils.create_attribute_type('TIKTOK_LOGS_BODY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Body", self.case)
        



        # self.attributes = {}
        # self.attributes["log_time"]= self.utils.create_attribute_type('TIKTOK_LOGS_TIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG, "Time", self.case)
        # # self.attributes["log_time"] 


        # self.attributes["log_time"]
        # Create artifacts
        
        self.art_messages = self.utils.create_artifact_type(self.module_name, "TIKTOK_MESSAGES","Messages", self.case)
        self.art_user_profile = self.utils.create_artifact_type(self.module_name, "TIKTOK_PROFILE", "Profile", self.case)
        self.art_profiles = self.utils.create_artifact_type(self.module_name, "TIKTOK_PROFILES_", "Profiles", self.case)
        self.art_searches = self.utils.create_artifact_type(self.module_name, "TIKTOK_SEARCHES","Search", self.case)
        self.art_videos = self.utils.create_artifact_type(self.module_name, "TIKTOK_VIDEOS", "Videos", self.case)
        self.art_undark = self.utils.create_artifact_type(self.module_name, "TIKTOK_UNDARK", "Undark", self.case)
        self.art_logs = self.utils.create_artifact_type(self.module_name, "TIKTOK_LOGS", "LOGS", self.case)
        
    def process_user_profile(self, profile, file):
        if not profile:
            return

        try: 
            self.log(Level.INFO, self.module_name + " Parsing user profile")
            art = file.newArtifact(self.art_user_profile.getTypeID())
            attributes = []

            #attributes = ArrayList()
            attributes.append(BlackboardAttribute(self.att_prf_account_region, self.module_name, profile.get("account_region")))
            attributes.append(BlackboardAttribute(self.att_prf_follower_count, self.module_name, profile.get("follower_count")))
            attributes.append(BlackboardAttribute(self.att_prf_following_count, self.module_name, profile.get("following_count")))
            attributes.append(BlackboardAttribute(self.att_prf_google_account, self.module_name, profile.get("google_account")))
            # attributes.append(BlackboardAttribute(self.att_prf_is_blocked, self.module_name, profile.get("is_blocked")))
            # attributes.append(BlackboardAttribute(self.att_prf_is_minor, self.module_name, profile.get("is_minor")))
            attributes.append(BlackboardAttribute(self.att_prf_nickname, self.module_name, profile.get("nickname")))
            attributes.append(BlackboardAttribute(self.att_prf_register_time, self.module_name, profile.get("register_time")))
            attributes.append(BlackboardAttribute(self.att_prf_sec_uid, self.module_name, profile.get("sec_uid")))
            attributes.append(BlackboardAttribute(self.att_prf_short_id, self.module_name, profile.get("short_id")))
            attributes.append(BlackboardAttribute(self.att_prf_uid, self.module_name, profile.get("uid")))
            attributes.append(BlackboardAttribute(self.att_prf_unique_id, self.module_name, profile.get("unique_id")))
        
            art.addAttributes(attributes)
            self.utils.index_artifact(self.case.getBlackboard(), art, self.art_user_profile)        
        except Exception as e:
            self.log(Level.INFO, self.module_name + " Error getting user profile: " + str(e))

    def process_messages(self, conversations, file):
        if not conversations:
            return
        try:
            
            for m in conversations:
                self.log(Level.INFO, self.module_name + " Parsing a new message")
                art = file.newArtifact(self.art_messages.getTypeID())
                
                participant_1 = m.get("participant_1")
                participant_2 = m.get("participant_2")
                
                for m in conversations.get("messages"):
                    attributes = []
                    attributes.append(BlackboardAttribute(self.att_msg_participant_1, self.module_name, participant_1))
                    attributes.append(BlackboardAttribute(self.att_msg_participant_2, self.module_name, participant_2))

                    attributes.append(BlackboardAttribute(self.att_msg_sender, self.module_name, m.get("sender")))
                    attributes.append(BlackboardAttribute(self.att_msg_created_time, self.module_name, m.get("createdtime")))
                    attributes.append(BlackboardAttribute(self.att_msg_type, self.module_name, m.get("type")))
                    attributes.append(BlackboardAttribute(self.att_msg_message, self.module_name, m.get("message")))
                    attributes.append(BlackboardAttribute(self.att_msg_read_status, self.module_name, m.get("readstatus")))
                    attributes.append(BlackboardAttribute(self.att_msg_local_info, self.module_name, m.get("localinfo")))
                    attributes.append(BlackboardAttribute(self.att_msg_deleted, self.module_name, m.get("deleted")))
                
                    art.addAttributes(attributes)
                    self.utils.index_artifact(self.case.getBlackboard(), art, self.art_messages)        
        except Exception as e:
            self.log(Level.INFO, self.module_name + " Error getting a message: " + str(e))


    def process_searches(self, searches, file):
        if not searches:
            return

        for s in searches:
            try: 
                self.log(Level.INFO, self.module_name + " Parsing a new search")
                art = file.newArtifact(self.art_searches.getTypeID())
                attributes = []
                attributes.append(BlackboardAttribute(self.att_searches, self.module_name, s))
                art.addAttributes(attributes)
                self.utils.index_artifact(self.case.getBlackboard(), art, self.art_searches)        
            except Exception as e:
                self.log(Level.INFO, self.module_name + " Error getting a search entry: " + str(e))

    def process_undark(self, undarks, file):
        if not undarks:
            return

        for database, row in undarks.items():
            try: 
                self.log(Level.INFO, self.module_name + " Parsing a new undark entry")
                art = file.newArtifact(self.art_undark.getTypeID())
                attributes = []
                attributes.append(BlackboardAttribute(self.att_undark_key, self.module_name, database))
                attributes.append(BlackboardAttribute(self.att_undark_output, self.module_name, row))
                art.addAttributes(attributes)
                self.utils.index_artifact(self.case.getBlackboard(), art, self.art_undark)        
            except Exception as e:
                self.log(Level.INFO, self.module_name + " Error getting a message: " + str(e))

    def process_users(self, users, file):
        if not users:
            return

        for u in users.items():
            try: 
                self.log(Level.INFO, self.module_name + " Parsing a new user")
                art = file.newArtifact(self.art_profiles.getTypeID())
                attributes = []
                attributes.append(BlackboardAttribute(self.att_prf_uid, self.module_name, u.get("uid")))
                attributes.append(BlackboardAttribute(self.att_prf_unique_id, self.module_name, u.get("uniqueid")))
                attributes.append(BlackboardAttribute(self.att_prf_nickname, self.module_name, u.get("nickname")))
                attributes.append(BlackboardAttribute(self.att_prf_avatar, self.module_name, u.get("avatar")))
                attributes.append(BlackboardAttribute(self.att_prf_follow_status, self.module_name, u.get("follow_status")))
                attributes.append(BlackboardAttribute(self.att_prf_url, self.module_name, u.get("url")))
            
                art.addAttributes(attributes)
                self.utils.index_artifact(self.case.getBlackboard(), art, self.art_profiles)        
            except Exception as e:
                self.log(Level.INFO, self.module_name + " Error getting user: " + str(e))
    
    def process_videos(self, videos, report_number, file, base_path, datasource_name):
        for v in videos:
            try: 
                self.log(Level.INFO, self.module_name + " Parsing a new video")
                art = file.newArtifact(self.art_videos.getTypeID())
                attributes = []
                attributes.append(BlackboardAttribute(self.att_vid_key, self.module_name, v.get("key")))
                attributes.append(BlackboardAttribute(self.att_vid_last_modified, self.module_name, v.get("last_modified")))
                art.addAttributes(attributes)
                self.utils.index_artifact(self.case.getBlackboard(), art, self.art_videos)        
            except Exception as e:
                self.log(Level.INFO, self.module_name + " Error getting a video: " + str(e))

        path = os.path.join(base_path, "Contents", "internal", "cache", "cache")
        try:
            files = os.listdir(path)
        except:
            self.log(Level.INFO, "Report {} doesn't have video files")
            return
        
        for v in files:
            self.log(Level.INFO, os.path.join(path, v))
            os.rename(os.path.join(path, v), os.path.join(path, v) + ".mp4")

        self.utils.add_to_fileset("{}_Videos".format(datasource_name), [path])



    def process_logs(self, logs, file):
        if not logs:
            return

        for l in logs:
            try: 
                self.log(Level.INFO, self.module_name + " Parsing a new log")
                art = file.newArtifact(self.art_logs.getTypeID())
                attributes = []
                attributes.append(BlackboardAttribute(self.att_log_action, self.module_name, l.get("action")))
                attributes.append(BlackboardAttribute(self.att_log_time, self.module_name, l.get("time")))
                attributes.append(BlackboardAttribute(self.att_log_session, self.module_name, l.get("session_id")))
                attributes.append(BlackboardAttribute(self.att_log_body, self.module_name, str(l.get("body"))))
            
                art.addAttributes(attributes)
                self.utils.index_artifact(self.case.getBlackboard(), art, self.art_logs)        
            except Exception as e:
                self.log(Level.INFO, self.module_name + " Error getting log: " + str(e))
