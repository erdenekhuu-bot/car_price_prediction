import React, { useState, useId, useEffect } from "react";
import {
  Layout,
  theme,
  Button,
  Table,
  ConfigProvider,
  Flex,
  Spin,
  Form,
  Image,
  Switch,
} from "antd";
import axios from "axios";
import { useQuery, useMutation } from "@tanstack/react-query";
import cabriolet from "./images/cabriolet.jpg";
import couple from "./images/couple.jpg";
import goodswagon from "./images/goodswagon.jpg";
import hatchback from "./images/hatchback.jpg";
import jeep from "./images/jeep.jpg";
import microbus from "./images/microbus.jpg";
import minivan from "./images/minivan.jpg";
import pickup from "./images/pickup.jpg";
import sedan from "./images/sedan.jpg";
import universal from "./images/universal.jpg";
import { useTranslation } from "react-i18next";

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const id = useId();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
  });
  const { t, i18n } = useTranslation();
  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const [checkout, setCheckout] = useState(true);
  const [form] = Form.useForm();
  const [listCategory, setListCategory] = useState<string[]>([]);

  const { data, isLoading } = useQuery({
    queryKey: ["list", id, pagination.current, pagination.pageSize],
    queryFn: async () => {
      const res = await axios.get("http://127.0.0.1:8000/api/", {
        params: {
          page: pagination.current,
          page_size: pagination.pageSize,
        },
      });
      return res.data;
    },
  });

  const mutation = useMutation({
    mutationFn: async (newCar: { id: string }) => {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/prediction/",
        newCar,
      );

      return res.data;
    },
  });

  const checkoutImage = (cat: string) => {
    const formatted = cat.toLowerCase().replace(/\s+/g, "");
    switch (formatted) {
      case "cabriolet":
        return cabriolet;
      case "coupe":
        return couple;
      case "goodswagon":
        return goodswagon;
      case "hatchback":
        return hatchback;
      case "jeep":
        return jeep;
      case "microbus":
        return microbus;
      case "minivan":
        return minivan;
      case "pickup":
        return pickup;
      case "sedan":
        return sedan;
      case "universal":
        return universal;
      default:
        return "";
    }
  };

  useEffect(() => {
    if (mutation.data) {
      setListCategory(mutation.data.list_category);
      form.setFieldsValue({
        price: mutation.data.predicted_price,
        currency: mutation.data.currency,
        confidence: mutation.data.confidence,
        category: mutation.data.category,
        fuel_type: mutation.data.fuel_type,
        mileage: mutation.data.mileage,
        list_category: mutation.data.list_category,
        evaluated: mutation.data.evaluated,
      });
    }
  }, [mutation.data, form]);

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#00b96b",
          colorBgContainer,
          borderRadiusLG,
        },
      }}
    >
      <Layout className="!h-screen !flex !flex-row-reverse">
        <Sider
          trigger={null}
          width={500}
          collapsible
          collapsed={checkout}
          className="!bg-[#1f1f1f] !z-10 !overflow-hidden !transition-all !duration-300"
        >
          {!checkout && (
            <Flex
              vertical
              justify="space-between"
              align="center"
              className="!h-full !p-6"
            >
              <div className="w-full flex-1 flex justify-center items-center">
                {mutation.isPending ? (
                  <Spin description={`${t("loading")}...`} size="large" />
                ) : (
                  <Form
                    form={form}
                    initialValues={mutation.data}
                    layout="vertical"
                    className="!w-3/4"
                  >
                    <Image
                      src={
                        mutation.data?.category &&
                        listCategory.includes(mutation.data.category)
                          ? checkoutImage(mutation.data.category)
                          : undefined
                      }
                      alt="Car category"
                    />
                    <p className="text-center text-5xl font-bold text-green-500 mb-12">
                      {mutation.data?.price}
                    </p>
                    <p className="text-xl font-bold text-white">
                      {" "}
                      {t("result")}:{" "}
                    </p>
                    <Form.Item label="Price" name="price">
                      <Flex gap={8}>
                        <span className="text-base font-medium text-white">
                          {t("price")}:
                        </span>
                        <span className="text-base text-white">
                          {mutation.data?.price}
                        </span>
                      </Flex>
                    </Form.Item>
                    <Form.Item label="" name="currency">
                      <Flex gap={8}>
                        <span className="text-base font-medium text-white">
                          {t("currency")}:
                        </span>
                        <span className="text-base text-white">
                          {mutation.data?.currency}
                        </span>
                      </Flex>
                    </Form.Item>

                    <Form.Item label="" name="category">
                      <Flex gap={8}>
                        <span className="text-base font-medium text-white">
                          {t("category")}:
                        </span>
                        <span className="text-base text-white">
                          {mutation.data?.category}
                        </span>
                      </Flex>
                    </Form.Item>

                    <Form.Item label="" name="fuel_type">
                      <Flex gap={8}>
                        <span className="text-base font-medium text-white">
                          {t("fueltype")}:
                        </span>
                        <span className="text-base text-white">
                          {mutation.data?.fuel_type}
                        </span>
                      </Flex>
                    </Form.Item>
                    <Form.Item label="" name="mileage">
                      <Flex gap={8}>
                        <span className="text-base font-medium text-white">
                          {t("mileage")}:
                        </span>
                        <span className="text-base text-white">
                          {`${mutation.data?.mileage} km`}
                        </span>
                      </Flex>
                    </Form.Item>
                    <Form.Item label="" name="evaluated">
                      <span className="text-base font-medium text-white">
                        <Flex gap={8}>
                          <span className="text-base font-medium text-white">
                            {t("evaluated")}:
                          </span>
                          <span className="text-base text-white">
                            {mutation.data?.evaluated}
                          </span>
                        </Flex>
                      </span>
                    </Form.Item>
                  </Form>
                )}
              </div>

              <Button block onClick={() => setCheckout(true)}>
                {t("back")}
              </Button>
            </Flex>
          )}
        </Sider>

        <Layout>
          <Header style={{ padding: 0, background: colorBgContainer }}>
            <Flex justify="end" align="center" className="!h-full !px-6">
              <Switch
                defaultChecked
                onChange={(checked) => changeLanguage(checked ? "mn" : "en")}
              />
            </Flex>
          </Header>

          <Content
            style={{
              margin: "24px 16px",
              padding: 24,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Table
              loading={isLoading}
              dataSource={data?.results || []}
              columns={[
                {
                  title: t("manufacturer"),
                  dataIndex: "manufacturer",
                  key: "manufacturer",
                },
                {
                  title: t("model"),
                  dataIndex: "model",
                  key: "model",
                },
                {
                  title: t("production_year"),
                  dataIndex: "prod_year",
                  key: "prod_year",
                },
                {
                  title: t("fuel_type"),
                  dataIndex: "fuel_type",
                  key: "fuel_type",
                },
                {
                  title: t("engine_volume"),
                  dataIndex: "engine_volume",
                  key: "engine_volume",
                },
                {
                  title: t("mileage"),
                  dataIndex: "mileage",
                  key: "mileage",
                },
                {
                  title: "",
                  dataIndex: "id",
                  key: "id",
                  render: (id) => (
                    <Button
                      type="primary"
                      onClick={() => {
                        setCheckout(false);
                        mutation.mutate({ id });
                      }}
                    >
                      {t("action")}
                    </Button>
                  ),
                },
              ]}
              bordered
              rowKey={"id"}
              pagination={{
                current: pagination.current,
                pageSize: pagination.pageSize,
                total: data?.count || 0,
                showSizeChanger: true,
                onChange: (page, pageSize) => {
                  setPagination({ current: page, pageSize });
                },
              }}
            />
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
};

export default App;
