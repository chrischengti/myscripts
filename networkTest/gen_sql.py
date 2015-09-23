#!/usr/bin/env python
import time
from string import Template
import simplejson as json

def gen_icmp_sql(infos):
    sql_tpl = "insert into gb_task (name,type,target,start_time,end_time,options,status,user_id,user_group_id,`interval`,priority,create_time) select '${from_name}T${to_name}',type,'${to_ip}',now(),'2015-04-30 00:00:00',options,status,user_id,user_group_id,`interval`,priority,now() from gb_task where id=33018;\ninsert into gb_task_locate_map (task_id,assign_type,assign_id,isp_id,max_assign_count,is_enabled) select a.id,b.assign_type,${from_clientid},b.isp_id,b.max_assign_count,b.is_enabled from gb_task as a,gb_task_locate_map as b where a.name='${from_name}T${to_name}' and b.task_id=33018;"

    sql_results = ""
    topos = ""

    # icmp sql in one region
    for provider, provider_infos in infos.items():
        for region, region_list in provider_infos.items():
            for (from_name, from_clientid, from_ip) in region_list:
                for (to_name, to_clientdid, to_ip) in region_list:
                    if from_name == to_name:
                        continue
                    key_values = {"from_name" : from_name, "to_name" : to_name, "to_ip" : to_ip, "from_clientid" : from_clientid}
                    sql_result = Template(sql_tpl).substitute(key_values)
                    sql_results += sql_result + "\n"
                    topos += "%s\t%s\n" %(from_name, to_name)
            
    # icmp sql between regions
    for provider, provider_infos in infos.items():    
        for from_region, from_region_list in provider_infos.items():
            for to_region, to_region_list in provider_infos.items():
                if from_region == to_region:
                    continue
                from_name, from_clientid, from_ip = from_region_list[0]
                to_name, to_clientid, to_ip = to_region_list[-1]
                key_values = {"from_name" : from_name, "to_name" : to_name, "to_ip" : to_ip, "from_clientid" : from_clientid}
                sql_result = Template(sql_tpl).substitute(key_values)
                sql_results += sql_result + "\n"
                topos += "%s\t%s\n" %(from_name, to_name)
    output_file = "sql_result.%s" %(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    topo_file = "topo.%s" %(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    file(output_file, "w").write(sql_results)
    file(topo_file, "w").write(topos)
    print "topo : %s" %(topo_file)
    print "output file : %s" %(output_file)
    
def gen_ecs_oss_sql(infos):
    sql_tpl = "insert into gb_task (name,type,target,start_time,end_time,options,status,user_id,user_group_id,`interval`,priority,create_time) select '${from_name}T${to_name}',type,'http://jingpin.bat',now(),'2015-04-30 00:00:00','{\"http_method\":\"GET\",\"http_cookie\":\"@echo off;cd \\\"%~dp0%osscmd_network\\\";osscmd_network.exe  -H ${to_name}\",\"http_gzip\":true,\"http_follow_302\":true,\"use_idc_client\":false}',status,user_id,user_group_id,`interval`,priority,now() from gb_task where id=37028;\ninsert into gb_task_locate_map (task_id,assign_type,assign_id,isp_id,max_assign_count,is_enabled) select a.id,b.assign_type,${from_clientid},b.isp_id,b.max_assign_count,b.is_enabled from gb_task as a,gb_task_locate_map as b where a.name='${from_name}T${to_name}' and b.task_id=37028;"
    oss_hosts_external = ["oss-cn-qingdao.aliyuncs.com",
                          "oss-cn-beijing.aliyuncs.com",
                          "oss-cn-hangzhou.aliyuncs.com",
                          "oss-cn-hongkong.aliyuncs.com",
                          "oss-cn-shenzhen.aliyuncs.com",
                          "oss-us-west-1.aliyuncs.com"]
    oss_hosts_internal = ["oss-cn-qingdao-internal.aliyuncs.com",
                          "oss-cn-beijing-internal.aliyuncs.com",
                          "oss-cn-hangzhou-internal.aliyuncs.com",
                          "oss-cn-hongkong-internal.aliyuncs.com",
                          "oss-cn-shenzhen-internal.aliyuncs.com",
                          "oss-us-west-1-internal.aliyuncs.com"]
    sql_results = ""
    topos = ""

    for region, region_list in infos.get("aliyun").items():
        for (from_name, from_clientid, from_ip) in region_list:
            for to_name in oss_hosts_external:
                key_values = {"from_name" : from_name, "to_name" : to_name, "from_clientid" : from_clientid}
                sql_result = Template(sql_tpl).substitute(key_values)
                sql_results += sql_result + "\n"
                topos += "%s\t%s\n" %(from_name, to_name)
    output_file = "sql_result.%s" %(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    topo_file = "topo.%s" %(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    file(output_file, "w").write(sql_results)
    file(topo_file, "w").write(topos)
    print "topo : %s" %(topo_file)
    print "output file : %s" %(output_file)
if __name__ == "__main__":
    '''
    input data sample 
    "aliyun_bj_1     101.200.73.187  11221103"
    "provider_region_index ip clientid"
    
    infos format
    {
    "ucloud": {
        "hd": [
            [
                "ucloud_hd_1",
                "11221127",
                "122.226.109.84"
            ],
            [
                "ucloud_hd_2",
                "11221128",
                "123.58.131.67"
            ]
        ],
        "bj": [
            [
                "ucloud_bj_1",
                "11221125",
                "123.59.55.219"
            ],
            [
                "ucloud_bj_2",
                "11221126",
                "123.59.55.218"
            ]
        ]
    }
    '''
    f = "region_ip"
    print "input file : %s" %(f)
    infos = {}
    for line in file(f).readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        name, ip, clientid = line.split()
        provider, region, index = name.split("_")
        detail = (name, clientid, ip)
        if infos.has_key(provider):
            provider_infos = infos[provider]
        else:
            provider_infos = {}
            infos[provider] = provider_infos
        if provider_infos.has_key(region):
            region_infos = provider_infos[region]
        else:
            region_infos = []
            provider_infos[region] = region_infos
        region_infos.append(detail)
    print json.dumps(infos, indent=4)
    gen_icmp_sql(infos)
    #gen_ecs_oss_sql(infos)

